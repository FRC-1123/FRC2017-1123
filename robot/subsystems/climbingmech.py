import ctre
from wpilib.command.subsystem import Subsystem

import robotmap
from commands.listenforclimb import ListenForClimb


class ClimbingMech(Subsystem):
    """
    This subsystem controls the 2 CAN Talons for the winch.
    """

    def __init__(self):
        super().__init__('Climbing Mechanism')

        self.motor = ctre.CANTalon(robotmap.climbing_mech.id)
        follower = ctre.CANTalon(robotmap.climbing_mech.follower_id)
        follower.setControlMode(ctre.CANTalon.ControlMode.Follower)
        follower.set(robotmap.climbing_mech.id)
        follower.setInverted(True)

    def setSpeed(self, speed):
        self.motor.set(speed)

    def initDefaultCommand(self):
        self.setDefaultCommand(ListenForClimb())
