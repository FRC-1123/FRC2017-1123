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
        self.requires(subsystems.gear_mech)

        self.sd = NetworkTables.getTable("SmartDashboard")

        # PID constants
        kp = 0.1
        ki = 0.0
        kd = 0.0
        # ktolerance = 2.0  # tolerance of 2 degrees per second
        self.rectified_drive = RectifiedDrive(kp, ki, kd)

    def execute(self):
        # tank drive
        # subsystems.motors.robot_drive.tankDrive(oi.joystick, robotmap.joystick.left_port, oi.joystick, robotmap.joystick.right_port, True)

        # arcade drive
        # subsystems.motors.robot_drive.arcadeDrive(oi.joystick)

        # rectified arcade drive
        power = oi.joystick.getY()
        angular_vel = oi.joystick.getX() * 360  # scale to maximum of 360 degrees per second
        self.rectified_drive.rectifiedDrive(power, angular_vel)
