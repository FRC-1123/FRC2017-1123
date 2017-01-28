import logging

import wpilib
from networktables import NetworkTables
from robotpy_ext.common_drivers import navx
from wpilib.command import Command

import robotmap
import subsystems

logging.basicConfig(level=logging.DEBUG)


class FollowJoystick(Command):
    '''
    This command will read the joysticks' y-axes and uses tank drive.
    '''

    def __init__(self):
        super().__init__('Follow Joystick')

        self.requires(subsystems.motors)
        self.requires(subsystems.oi)

    def execute(self):
        subsystems.motors.robot_drive.tankDrive(subsystems.oi.joystick, robotmap.joystick.left_port, subsystems.oi.joystick,
                                                robotmap.joystick.right_port, True)
