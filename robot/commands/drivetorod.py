import logging

from networktables import NetworkTables
from wpilib.command import PIDCommand

import subsystems
from commands.followjoystick import FollowJoystick
from commands.rumblecontroller import RumbleController
from inputs import camera
from inputs import oi
from inputs import sonar

logging.basicConfig(level=logging.INFO)


class DriveToRod(PIDCommand):
    """
    This command will find the rod and drive the robot towards it.
    """

    def __init__(self, power=0.3):
        self.sd = NetworkTables.getTable("SmartDashboard")

        # PID constants
        # kp = 0.01
        # ki = 0.005
        # kd = 0.002
        # kf = 0.0
        # ktolerance = 0.02

        # NetworkTables variables for tuning
        kp = self.sd.getNumber("rod/kp")
        ki = self.sd.getNumber("rod/ki")
        kd = self.sd.getNumber("rod/kd")
        kf = self.sd.getNumber("rod/kf")
        ktolerance = self.sd.getNumber("rod/ktolerance")

        # initialize PID controller with a period of 0.03 seconds
        super().__init__(kp, ki, kd, 0.03, kf, "Drive To Rod")

        self.requires(subsystems.motors)

        turnController = self.getPIDController()
        turnController.setInputRange(-1.0, 1.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(ktolerance)
        turnController.setContinuous(True)
        turnController.setSetpoint(0.5)  # want rod to be at center

        self.logger = logging.getLogger("robot")

        self.is_autonomous = self.sd.getBoolean("isautonomous")
        self.is_lost = False  # can't find the rod

        self.power = power
        self.last_output = 0  # for if the rod is lost

    def returnPIDInput(self):
        if oi.controller.getBackButton():  # return control back to controller
            FollowJoystick().start()
            return 0.5
        rod_pos = camera.get_rod_pos()
        if rod_pos is None:
            self.logger.critical("Couldn't find the rod!")
            self.is_lost = True
            if not self.is_autonomous:  # return control to controller if not in autonomous
                self.logger.critical("Returning control to the controller!")
                FollowJoystick().start()
                RumbleController(0.5).start()
            return 0.5
        else:
            self.sd.putNumber("rod/actual", rod_pos[0])
            return rod_pos[0]

    def usePIDOutput(self, output):
        if self.is_lost:  # if lost, slowly spin in circle
            # TODO: check signs of motor outputs
            if self.last_output > 0:  # keep turning right
                subsystems.motors.robot_drive.setLeftRightMotorOutputs(0.1, 0.1)
            else:  # keep turning left
                subsystems.motors.robot_drive.setLeftRightMotorOutputs(-0.1, -0.1)
        else:
            subsystems.motors.robot_drive.drive(self.power, output)
            self.last_output = output

    def isFinished(self):
        # stop when within 8 inches of the wall
        return sonar.front.get() < 8.0

    def end(self):
        subsystems.motors.robot_drive.setLeftRightMotorOutputs(0, 0)
