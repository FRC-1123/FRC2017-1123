import logging

import wpilib
from wpilib.command import PIDCommand

import cameras
import subsystems

logging.basicConfig(level=logging.INFO)


class DriveToRod(PIDCommand):
    """
    This command will find the rod and drive the robot towards it.
    """

    def __init__(self):
        # PID constants
        kp = 0.01
        ki = 0.0
        kd = 0.0
        kf = 0.0
        ktolerance = 0.02

        # initialize PID controller with a period of 0.05 seconds
        super().__init__(kp, ki, kd, 0.05, kf, "Drive To Rod")

        self.requires(subsystems.motors)

        turnController = self.getPIDController()
        turnController.setInputRange(-1.0, 1.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(ktolerance)
        turnController.setContinuous(True)

        self.logger = logging.getLogger("robot")

        # used for calculating PID derivative and integral
        self.timer = wpilib.Timer()
        self.timer.start()

    def returnPIDInput(self):
        rod_pos = cameras.front_camera.get_rod_pos()
        if rod_pos is None:
            self.logger.info("Couldn't find the rod!")
            return 0.0
        error = .5 - rod_pos[0]  # error as horizontal distance from center
        self.logger.info("current rod error: {}".format(error))
        return error

    def usePIDOutput(self, output):
        subsystems.motors.robot_drive.drive(.5, output)
