import ctre
import wpilib
from networktables import NetworkTables
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
        self.left_motor.setControlMode(ctre.CANTalon.ControlMode.Speed)
        self.left_motor.setFeedbackDevice(ctre.CANTalon.FeedbackDevice.QuadEncoder)
        self.left_motor.setInverted(True)
        self.right_motor = ctre.CANTalon(robotmap.motors.right_id)
        self.right_motor.setControlMode(ctre.CANTalon.ControlMode.Speed)
        self.right_motor.setFeedbackDevice(ctre.CANTalon.FeedbackDevice.QuadEncoder)
        self.right_motor.setInverted(True)

        self.left_motor.setPID(p=0.3, i=0, d=0, f=0, izone=0)
        self.right_motor.setPID(p=0.3, i=0, d=0, f=0, izone=0)

        self.sd = NetworkTables.getTable("SmartDashboard")
        self.sd.putNumber("direction", 1)

        # follower motors
        left_motor_follower = ctre.CANTalon(robotmap.motors.left_follower_id)
        left_motor_follower.setControlMode(ctre.CANTalon.ControlMode.Follower)
        left_motor_follower.set(robotmap.motors.left_id)
        right_motor_follower = ctre.CANTalon(robotmap.motors.right_follower_id)
        right_motor_follower.setControlMode(ctre.CANTalon.ControlMode.Follower)
        right_motor_follower.set(robotmap.motors.right_id)

        self.robot_drive = wpilib.RobotDrive(self.left_motor, self.right_motor)
        self.robot_drive.setMaxOutput(0.69)  # maximum edges per 10ms

    def forwardDirection(self):
        if self.sd.getNumber("direction") == -1:
            tmp = self.left_motor
            self.left_motor = self.right_motor
            self.right_motor = tmp
            self.left_motor.setInverted(True)
            self.right_motor.setInverted(True)
            # self.robot_drive.rearLeftMotor = self.left_motor
            # self.robot_drive.rearRightMotor = self.right_motor
            self.robot_drive.free()
            self.robot_drive = wpilib.RobotDrive(self.left_motor, self.right_motor)
            self.robot_drive.setMaxOutput(1)
        self.sd.putNumber("direction", 1)

    def reverseDirection(self):
        if self.sd.getNumber("direction") == 1:
            tmp = self.left_motor
            self.left_motor = self.right_motor
            self.right_motor = tmp
            self.left_motor.setInverted(False)
            self.right_motor.setInverted(False)
            # self.robot_drive.rearLeftMotor = self.left_motor
            # self.robot_drive.rearRightMotor = self.right_motor
            self.robot_drive.free()
            self.robot_drive = wpilib.RobotDrive(self.left_motor, self.right_motor)
            self.robot_drive.setMaxOutput(1)
        self.sd.putNumber("direction", -1)

    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
