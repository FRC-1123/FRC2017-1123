import logging

from networktables import NetworkTables
from wpilib.command import Command

import oi
import subsystems
from rectifieddrive import RectifiedDrive

logging.basicConfig(level=logging.DEBUG)


class FollowJoystick(Command):
    """
    This command will read the joysticks' y-axes and uses tank drive.
    """

    def __init__(self):
        super().__init__('Follow Joystick')

        self.requires(subsystems.motors)
        # self.requires(subsystems.gear_mech)

        self.sd = NetworkTables.getTable("SmartDashboard")

        self.logger = logging.getLogger("robot")

        # PID constants
        kp = 0.01
        ki = 0.0
        kd = 0.0
        tolerance = 0.05  # tolerance for driving straight forward
        self.drive = RectifiedDrive(kp, ki, kd, tolerance, 100)

    def execute(self):
        # tank drive
        # subsystems.motors.robot_drive.tankDrive(oi.joystick, robotmap.joystick.left_port, oi.joystick,
        #                                         robotmap.joystick.right_port, True)

        # arcade drive
        # subsystems.motors.robot_drive.arcadeDrive(oi.joystick)

        # rectified arcade drive
        power = oi.joystick.getY()
        angular_vel = -oi.joystick.getX()
        self.logger.info(angular_vel)
        # self.logger.info(angular_vel)
        self.drive.rectified_drive(power, angular_vel)
