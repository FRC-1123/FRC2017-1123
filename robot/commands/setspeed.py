import wpilib
from wpilib.command import TimedCommand

import subsystems


class SetSpeed(TimedCommand):
    """
    Spins the motors at the given power for a given number of seconds and then stops.
    """

    def __init__(self, power, timeoutInSeconds):
        super().__init__('Set Speed %d' % power, timeoutInSeconds)

        self.power = power
        self.requires(subsystems.motors)

        self.timer = wpilib.Timer()
        self.timer.start()

    def execute(self):
        subsystems.motors.setSpeed(self.power)
        self.timer.delay(0.05)

    def end(self):
        subsystems.motors.setSpeed(0)
