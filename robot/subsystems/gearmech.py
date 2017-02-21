import wpilib
from wpilib.command.subsystem import Subsystem

import robotmap


class GearMech(Subsystem):
    """
    This subsystem controls the gear mechanism's piston.
    """

    def __init__(self):
        super().__init__('GearMech')

        self.double_solenoid = wpilib.DoubleSolenoid(robotmap.gear_mech.forward_solenoid_channel, robotmap.gear_mech.reverse_solenoid_channel)
