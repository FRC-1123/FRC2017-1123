#!/usr/bin/env python3

import logging

import wpilib
from commandbased import CommandBasedRobot
from networktables import NetworkTables

import subsystems
from commands.autonomous import AutonomousProgram
from commands.updatenetworktables import UpdateNetworkTables
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
        self.sd = NetworkTables.getTable("SmartDashboard")

        # set autonomous modes
        self.sd.putStringArray("autonomous/options", ["left", "center", "right"])
        self.sd.putString("autonomous/selected", "center")

        # drive-to-rod PID values (for tuning)
        self.sd.putNumber("rod/kp", 0.01)
        self.sd.putNumber("rod/ki", 0.005)
        self.sd.putNumber("rod/kd", 0.002)
        self.sd.putNumber("rod/kf", 0.0)
        self.sd.putNumber("rod/ktolerance", 0.02)

        # RectifiedDrive PID values (for tuning)
        self.sd.putNumber("drive/kp", 0.01)
        self.sd.putNumber("drive/ki", 0.005)
        self.sd.putNumber("drive/kd", 0.002)
        self.sd.putNumber("drive/kf", 0.0)
        self.sd.putNumber("drive/ktolerance", 0.1)

        navx.init()
        oi.init()
        wpilib.CameraServer.launch('inputs/camera.py:start')

    def autonomousInit(self):
        global is_autonomous
        is_autonomous = True
        UpdateNetworkTables().start()
        if self.sd.containsKey("autonomous/selected"):
            AutonomousProgram(self.sd.getString("autonomous/selected")).start()
        else:  # if not set for some reason (bad!), just use center mode
            AutonomousProgram("center").start()
        self.logger.info("Started autonomous.")

    def teleopInit(self):
        global is_autonomous
        is_autonomous = False
        self.sd.putBoolean("timeRunning", True)  # start dashboard timer
        # RespondToController().start()
        UpdateNetworkTables().start()
        # ServeStream().start()
        self.logger.info("Started teleop.")


if __name__ == '__main__':
    wpilib.run(Robot)
