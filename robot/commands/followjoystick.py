import logging

from networktables import NetworkTables
from wpilib.command import Command

import subsystems
from inputs import oi
from rectifieddrive import RectifiedDrive

logging.basicConfig(level=logging.INFO)

class FollowJoystick(Command):
    """
    This command will read the joysticks' y-axes and uses tank drive.
    """

    def __init__(self):
        super().__init__('Follow Joystick')

        self.requires(subsystems.motors)

        self.sd = NetworkTables.getTable("SmartDashboard")

        self.logger = logging.getLogger("robot")

        self.drive = RectifiedDrive(100, period=0.02)

    def execute(self):
        # tank drive
        # subsystems.motors.robot_drive.tankDrive(oi.joystick, robotmap.joystick.left_port, oi.joystick,
        #                                         robotmap.joystick.right_port, True)

        # arcade drive
        # subsystems.motors.robot_drive.arcadeDrive(oi.joystick)

        # rectified arcade drive
        power = oi.joystick.getRawAxis(4)
        angular_vel = -oi.joystick.getRawAxis(5)
        self.logger.info(angular_vel)
        self.drive.rectified_drive(power, angular_vel)
