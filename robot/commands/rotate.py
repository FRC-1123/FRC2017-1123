import wpilib
from robotpy_ext.common_drivers.navx import AHRS
from wpilib.command import Command

import subsystems


class Rotate(Command):
    """
    This command uses the NavX to rotate to the specified angle.
    """

    def __init__(self, angle):
        super().__init__("Rotate to angle {}".format(angle))

        self.angle = angle
        self.requires(subsystems.motors)

        self.ahrs = AHRS.create_spi()

        # PID constants
        self.kp = 0.06
        self.ki = 0.0
        self.kd = 0.0
        self.kf = 0.0
        self.ktolerance = 2.0

        self.turnController = wpilib.PIDController(self.kp, self.ki, self.kd, self.kf, self.ahrs, output=self)
        self.turnController.setInputRange(-180.0, 180.0)
        self.turnController.setOutputRange(-1.0, 1.0)
        self.turnController.setAbsoluteTolerance(self.ktolerance)
        self.turnController.setContinuous(True)

        self.rotateToAngleRate = 0.0
        self.turnController.setSetpoint(angle)

        # Add the PID Controller to the Test-mode dashboard, allowing manual  */
        # tuning of the Turn Controller's P, I and D coefficients.            */
        # Typically, only the P value needs to be modified.                   */
        wpilib.LiveWindow.addActuator("DriveSystem", "RotateController", turnController)

    def execute(self):
        self.turnController.enable()
        currentRotationRate = self.rotateToAngleRate

        subsystems.motors.robot_drive.drive(0.5, currentRotationRate)

        # wpilib.Timer.delay(0.005) # wait for a motor update time

    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        self.rotateToAngleRate = output
