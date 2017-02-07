#!/usr/bin/env python3

import logging

import wpilib
from commandbased import CommandBasedRobot
from networktables import NetworkTables

import subsystems
from commands.autonomous import AutonomousProgram
from commands.servestream import ServeStream
from commands.updatenetworktables import UpdateNetworkTables
from inputs import cameras
from inputs import navx
from inputs import oi

is_autonomous = False

class Robot(CommandBasedRobot):
    def robotInit(self):
        """
        Set up everything.
        """

        subsystems.init()

        self.logger = logging.getLogger("robot")

        navx.init()
        oi.init()
        cameras.init()

        ServeStream().start()

    def autonomousInit(self):
        global is_autonomous
        is_autonomous = True
        AutonomousProgram().start()
        self.logger.info("Started autonomous.")

    def teleopInit(self):
        global is_autonomous
        is_autonomous = False
        sd = NetworkTables.getTable("SmartDashboard")
        sd.putBoolean("timeRunning", True)  # start dashboard timer
        # RespondToController().start()
        UpdateNetworkTables().start()
        self.logger.info("Started teleop.")


if __name__ == '__main__':
    wpilib.run(Robot)
