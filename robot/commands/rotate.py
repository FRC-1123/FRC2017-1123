import logging

from wpilib.command import PIDCommand

import subsystems
from inputs import navx


class Rotate(PIDCommand):
    """
    This command uses the NavX to rotate to the specified angle.
    """

    def __init__(self, angle):
        # PID constants
        kp = 0.007
        ki = 0.001
        kd = 0.05
        kf = 0.0
        ktolerance = 1.0  # tolerance of 1.0 degree

        # initialize PID controller with a period of 0.05 seconds
        super().__init__(kp, ki, kd, 0.05, kf, "Rotate to angle {}".format(angle))

        self.requires(subsystems.motors)

        self.initial_angle = navx.ahrs.getAngle()
        self.rate = 1.0

        turn_controller = self.getPIDController()
        turn_controller.setInputRange(-180, 180)
        turn_controller.setOutputRange(-1.0, 1.0)
        turn_controller.setAbsoluteTolerance(ktolerance)
        turn_controller.setContinuous(True)
        turn_controller.setSetpoint(angle)

        self.logger = logging.getLogger('robot')

    def returnPIDInput(self):
        return navx.ahrs.getAngle() - self.initial_angle

    def usePIDOutput(self, output):
        self.rate = output
        subsystems.motors.robot_drive.setLeftRightMotorOutputs(output, -output)

    def isFinished(self):
        # stop command if rate set to less than 0.02 or if it has been 2 seconds
        if abs(self.rate) < 0.02 or self.timeSinceInitialized() > 2:
            self.logger.info("Done rotating {}.".format(self.rate))
            return True
        return False

    def end(self):
        # set outputs to 0 on end
        subsystems.motors.robot_drive.setLeftRightMotorOutputs(0, 0)
