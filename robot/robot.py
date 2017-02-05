#!/usr/bin/env python3

import logging

import wpilib
from commandbased import CommandBasedRobot
from networktables import NetworkTables

import cameras
import navx
import oi
import subsystems
from commands.autonomous import AutonomousProgram
from commands.respondtocontroller import RespondToController
from commands.servestream import ServeStream
from commands.updatenetworktables import UpdateNetworkTables

logging.basicConfig(level=logging.DEBUG)


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
        AutonomousProgram().start()
        self.logger.info("Started autonomous.")


    def teleopInit(self):
        sd = NetworkTables.getTable("SmartDashboard")
        sd.putBoolean("timeRunning", True)  # start dashboard timer
        UpdateNetworkTables().start()
        RespondToController().start()
        self.logger.info("Started teleop.")


if __name__ == '__main__':
    wpilib.run(Robot)
