import wpilib
from wpilib.command.subsystem import Subsystem

import robotmap


class Switches(Subsystem):
    def __init__(self):
        '''Instantiates the switch objects.'''

        super().__init__('Switch')

        self.limit_switch = wpilib.DigitalInput(robotmap.switches.limit_switch_channel)
