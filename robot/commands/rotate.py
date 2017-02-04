from wpilib.command import PIDCommand

import navx
import subsystems


class Rotate(PIDCommand):
    """
    This command uses the NavX to rotate to the specified angle.
    """

    def __init__(self, angle):
        # PID constants
        kp = 0.005
        ki = 0.0
        kd = 0.0
        kf = 0.0
        ktolerance = 2.0  # tolerance of 2 degrees

        # initialize PID controller with a period of 0.05 seconds
        super().__init__(kp, ki, kd, 0.05, kf, "Rotate to angle {}".format(angle))

        self.requires(subsystems.motors)

        self.rate = 1.0

        turn_controller = self.getPIDController()
        turn_controller.setInputRange(-180.0, 180.0)
        turn_controller.setOutputRange(-1.0, 1.0)
        turn_controller.setAbsoluteTolerance(ktolerance)
        turn_controller.setContinuous(True)
        # self.rotateToAngleRate = 0.0
        turn_controller.setSetpoint(angle)

        # Add the PID Controller to the Test-mode dashboard, allowing manual  */
        # tuning of the Turn Controller's P, I and D coefficients.            */
        # Typically, only the P value needs to be modified.                   */
        # wpilib.LiveWindow.addActuator("DriveSystem", "RotateController", self.turnController)

    def returnPIDInput(self):
        return navx.ahrs.getFusedHeading()

    def usePIDOutput(self, output):
        self.rate = output
        subsystems.motors.robot_drive.setLeftRightMotorOutputs(-output, output)

    def isFinished(self):
        return abs(self.rate) < 0.01
