import wpilib
from wpilib.command.subsystem import Subsystem

import robotmap


class Dumper(Subsystem):
    """
    This subsystem controls the ball dumper piston.
    """

    def __init__(self):
        super().__init__('Dumper')

        self.double_solenoid = wpilib.DoubleSolenoid(robotmap.dumper.forward_solenoid_channel, robotmap.dumper.reverse_solenoid_channel)
