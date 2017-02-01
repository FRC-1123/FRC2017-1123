import logging

from networktables import NetworkTables
from wpilib.command import Command

import oi
import robotmap
import subsystems

logging.basicConfig(level=logging.DEBUG)


class FollowJoystick(Command):
    """
    This command will read the joysticks' y-axes and uses tank drive.
    """

    def __init__(self):
        super().__init__('Follow Joystick')

        self.requires(subsystems.motors)
        self.requires(subsystems.gear_mech)

        self.sd = NetworkTables.getTable("SmartDashboard")

    def execute(self):
        # tank drive
        subsystems.motors.robot_drive.tankDrive(oi.joystick, robotmap.joystick.left_port, oi.joystick, robotmap.joystick.right_port, True)
