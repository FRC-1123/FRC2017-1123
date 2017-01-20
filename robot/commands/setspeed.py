from wpilib.command import TimedCommand

import subsystems

class SetSpeed(TimedCommand):
    '''
    Spins the motor at the given power for a given number of seconds, then
    stops.
    '''

    def __init__(self, power, timeoutInSeconds):
        super().__init__('Set Speed %d' % power, timeoutInSeconds)

        self.power = power
        self.requires(subsystems.motors)

    def initialize(self):
        subsystems.motors.setSpeed(self.power)


    def end(self):
        subsystems.motors.setSpeed(0)
