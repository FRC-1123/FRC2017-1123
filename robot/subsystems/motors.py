import wpilib
from wpilib.command.subsystem import Subsystem
import ctre

from commands.followjoystick import FollowJoystick
import robotmap


class Motors(Subsystem):
    '''
    This subsystem controls the CAN Talons.
    '''

    def __init__(self):
        '''Instantiates the motor objects.'''

        super().__init__('Motors')

        self.left_motor = ctre.CANTalon(robotmap.motors.left_id)
        self.right_motor = ctre.CANTalon(robotmap.motors.right_id)
        # self.left_motor = wpilib.Talon(robotmap.motors.left_id)
        # self.right_motor = wpilib.Talon(robotmap.motors.right_id)
        self.robot_drive = wpilib.RobotDrive(self.left_motor, self.right_motor)
        self.robot_drive.setMaxOutput(1)

    def setSpeed(self, speed):
        self.robot_drive.drive(speed, 0)

    def initDefaultCommand(self):
        self.setDefaultCommand(FollowJoystick())
