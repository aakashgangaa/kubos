#!/usr/bin/env python3

"""
Remove a task list from a mode in the scheduler. If the mode is active, all tasks in the task list will be removed from the schedule.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import app_api
import argparse
import sys

def main():

    logger = app_api.logging_setup("remove-task-list")

    # parse arguments for config file and run type
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', '-r', nargs=1)
    parser.add_argument('--config', '-c', nargs=1)
    args = parser.parse_args()

    if args.config is not None:
        # use user config file if specified in command line
        SERVICES = app_api.Services(args.config[0])
    else:
        # else use default global config file
        SERVICES = app_api.Services("/etc/kubos-config.toml")

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
    pass

# logic run when commanded by OBC
def on_command(logger, SERVICES):

    name = "task_name"
    mode = "mode_name"

    # send mutation to remove task list from mode in scheduler
    request = '''
    mutation {
        removeTaskList(name: "%s", mode: "%s") {
            success
            errors
        }
    }
    ''' % (name, mode)
    response = SERVICES.query(service="scheduler-service", query=request)

    # get results
    response = response["removeTaskList"]
    success = response["success"]
    errors = response["errors"]

    if success:
        logger.info("Removed task list {} from mode {}.".format(name, mode))
    else:
        logger.warning("Could not remove task list {} from mode {}: {}.".format(name, mode, errors))


if __name__ == "__main__":
    main()
