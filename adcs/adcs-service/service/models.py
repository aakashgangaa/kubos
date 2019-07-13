#!/usr/bin/env python3

"""
Graphene ObjectType classes for subsystem modeling.
"""

__author__ = "Jon Grebe"
__version__ = "0.1.0"
__license__ = "MIT"

import graphene

class Adcs(graphene.ObjectType):
    """
    Model encapsulating subsystem functionality.
    """

    power_on = graphene.Boolean()

    def refresh(self):
        """
        Will hold code for refreshing the status of the subsystem
        model based on queries to the actual hardware.
        """

        print("Querying for adcs status")
        self.power_on = not self.power_on

    def set_power_on(self, power_on):
        """
        Controls the power state of the adcs subsystem
        """

        print("Sending new power state to adcs")
        print("Previous State: {}".format(self.power_on))
        print("New State: {}".format(power_on))
        self.power_on = power_on
        return Status(status=True, subsystem=self)


class Status(graphene.ObjectType):
    """
    Model representing execution status. This allows us to return
    the status of the mutation function alongside the state of
    the model affected.
    """

    status = graphene.Boolean()
    subsystem = graphene.Field(Adcs)
