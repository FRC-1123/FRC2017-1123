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
        subsystems.motors.ignore_joy = True
        subsystems.motors.robot_drive.drive(self.power, 0)

    def end(self):
        subsystems.motors.setSpeed(0)
        subsystems.motors.ignore_joy = False
