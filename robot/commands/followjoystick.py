import logging

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

        self.drive = RectifiedDrive(30)

    def execute(self):
        # tank drive
        # subsystems.motors.robot_drive.tankDrive(oi.joystick, robotmap.joystick.left_port, oi.joystick,
        #                                         robotmap.joystick.right_port, True)

        # arcade drive
        # subsystems.motors.robot_drive.arcadeDrive(oi.joystick)

        # rectified arcade drive
        power = oi.joystick.getRawAxis(robotmap.joystick.forwardAxis)
        power /= 4
        angular_vel = -oi.joystick.getRawAxis(robotmap.joystick.steeringAxis)
        # if power > 0:  # if moving backwards, negate angular velocity
        #     angular_vel *= -1
        # self.logger.info("{}\t{}".format(angular_vel, power))
        self.drive.rectified_drive(power, angular_vel)
