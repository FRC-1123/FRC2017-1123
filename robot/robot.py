#!/usr/bin/env python3

import logging

# from inputs import cameras
from inputs import oi
import wpilib
from commandbased import CommandBasedRobot
from networktables import NetworkTables

import subsystems
from commands.autonomous import AutonomousProgram
from commands.respondtocontroller import RespondToController
# from commands.servestream import ServeStream
from commands.updatenetworktables import UpdateNetworkTables
from inputs import navx


class Robot(CommandBasedRobot):
    def robotInit(self):
        """
        Set up everything.
        """

        subsystems.init()

        self.logger = logging.getLogger("robot")

        navx.init()
        oi.init()
        # cameras.init()

        UpdateNetworkTables().start()
        # ServeStream().start()

    def autonomousInit(self):
        AutonomousProgram().start()
        self.logger.info("Started autonomous.")


    def teleopInit(self):
        sd = NetworkTables.getTable("SmartDashboard")
        sd.putBoolean("timeRunning", True)  # start dashboard timer
        RespondToController().start()
        self.logger.info("Started teleop.")


if __name__ == '__main__':
    wpilib.run(Robot)
