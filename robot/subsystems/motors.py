import ctre
import wpilib
from wpilib.command.subsystem import Subsystem

import robotmap
from commands.followjoystick import FollowJoystick


class Motors(Subsystem):
    """
    This subsystem controls the 4 CAN Talons (two per wheel).
    """

    def __init__(self):
        """
        Instantiates the motor objects.
        """

        super().__init__('Motors')

        # main motors
        self.left_motor = ctre.CANTalon(robotmap.motors.left_id)
        self.right_motor = ctre.CANTalon(robotmap.motors.right_id)
        self.left_motor.setInverted(True)
        self.right_motor.setInverted(True)

        # follower motors
        left_motor_follower = ctre.CANTalon(robotmap.motors.left_follower_id)
        left_motor_follower.setControlMode(ctre.CANTalon.ControlMode.Follower)
        left_motor_follower.set(robotmap.motors.left_id)
        right_motor_follower = ctre.CANTalon(robotmap.motors.right_follower_id)
        right_motor_follower.setControlMode(ctre.CANTalon.ControlMode.Follower)
        right_motor_follower.set(robotmap.motors.right_id)

        self.robot_drive = wpilib.RobotDrive(self.left_motor, self.right_motor)
        self.robot_drive.setMaxOutput(1)

    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
