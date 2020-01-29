#!/usr/bin/env python3

"""
Main file for payload application that defines communcation between CDH and
primary payload (camera) mainly through hardware payload-service
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("payload-nominal")

    # parse arguments for config file and run type
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
    parser.add_argument('cmd_args', nargs='*')
    args = parser.parse_args()

    if args.config is not None:
        # use user config file if specified in command line
        SERVICES = app_api.Services(args.config[0])
    else:
        # else use default global config file
        SERVICES = app_api.Services()

    # run app onboot or oncommand logic
    if args.run is not None:
        if args.run[0] == 'OnBoot':
            on_boot(logger, SERVICES)
        elif args.run[0] == 'OnCommand':
            on_command(logger, SERVICES)
    else:
        on_command(logger, SERVICES)

# logic run for application on OBC boot
def on_boot(logger, SERVICES):
    logger.debug("Setting up payload subsystem...")
'''
code to setup/initialize payload subsystem
'''

# logic run when commanded by OBC
def on_command(logger, SERVICES):
    logger.info("Starting nominal operation for payload subsystem...")

    while True:
        # pinging payload subsystem
        request = '{ ping }'
        response = SERVICES.query(service="payload-service", query=request)
        response = response["ping"]

        if response == "pong":
            logger.debug("Successful connection to payload subsystem")
        else:
            logger.warn("Unsuccessful connection to payload subsystem. Sent: {} | Received: {}. Trying again...".format(request, response))

'''
code for continuous nominal operation for payload
'''

if __name__ == "__main__":
    main()
