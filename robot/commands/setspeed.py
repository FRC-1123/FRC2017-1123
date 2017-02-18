import wpilib
from wpilib.command import TimedCommand

import subsystems
from rectifieddrive import RectifiedDrive


class SetSpeed(TimedCommand):
    """
    Spins the motors at the given power for a given number of seconds and then stops.
    """

    def __init__(self, power, timeoutInSeconds):
        super().__init__('Set Speed %d' % power, timeoutInSeconds)

        self.requires(subsystems.motors)

        self.power = power
        self.drive = RectifiedDrive(0)
        self.timer = wpilib.Timer()
        self.timer.start()

    def execute(self):
        self.drive.rectified_drive(self.power, 0)
        # subsystems.motors.setSpeed(self.power)
        self.timer.delay(0.05)

    def end(self):
        # set outputs to 0 on end
        subsystems.motors.robot_drive.setLeftRightMotorOutputs(0, 0)
