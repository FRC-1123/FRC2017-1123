import wpilib
from wpilib.command.subsystem import Subsystem

import robotmap

class GearMech(Subsystem):
    '''
    This subsystem controls the gear mechanism.
    '''

    def __init__(self):
        super().__init__('GearMech')

        self.solenoid = wpilib.Solenoid(robotmap.gear_mech.solenoid_channel)
