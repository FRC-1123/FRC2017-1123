import logging

from networktables import NetworkTables
from wpilib import Timer
from wpilib.command import Command

import robotmap
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

        self.logger = logging.getLogger("robot")
        self.drive = RectifiedDrive(25, 0.05, squared_inputs=True)

        self.sd = NetworkTables.getTable("SmartDashboard")

        self.timer = Timer()
        self.timer.start()

    def execute(self):
        if self.timer.hasPeriodPassed(0.05):  # period of 0.05 seconds
            # tank drive
            # subsystems.motors.robot_drive.tankDrive(oi.joystick, robotmap.joystick.left_port, oi.joystick,
            #                                         robotmap.joystick.right_port, True)

            # arcade drive
            # subsystems.motors.robot_drive.arcadeDrive(oi.joystick)

            # rectified arcade drive
            power = -oi.joystick.getRawAxis(robotmap.joystick.forwardAxis) * 0.75
            angular_vel = oi.joystick.getRawAxis(robotmap.joystick.steeringAxis)

            if self.sd.contains("slowmode") and self.sd.getBoolean("slowmode"):
                power *= 0.75
                angular_vel *= 0.75
            if abs(angular_vel) < 0.05:  # tolerance
                angular_vel = 0
            self.drive.rectified_drive(power, angular_vel)

    def end(self):
        subsystems.motors.robot_drive.setLeftRightMotorOutputs(0, 0)
