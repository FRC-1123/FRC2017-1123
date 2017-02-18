import logging

import wpilib
from networktables import NetworkTables
from wpilib.command import Command

import subsystems
from commands.rotate import Rotate
from commands.setspeed import SetSpeed
from inputs import navx
from inputs import sonar

logging.basicConfig(level=logging.INFO)


class UpdateNetworkTables(Command):
    """
    This command updates NetworkTables variables.
    """

    def __init__(self):
        super().__init__('Update NetworkTables')

        self.logger = logging.getLogger("robot")

        self.sd = NetworkTables.getTable("SmartDashboard")
        self.nt_timer = wpilib.Timer()  # timer for updating NetworkTables
        self.nt_timer.start()

    def execute(self):
        if self.nt_timer.hasPeriodPassed(.2):  # update NetworkTables every 0.2 seconds
            # dashboard forward button (for demonstration purposes)
            if self.sd.containsKey("forwardCommand") and self.sd.getBoolean("forwardCommand"):  # check if move forward button pressed
                self.sd.putBoolean("forwardCommand", False)
                SetSpeed(0.5, 1).start()  # move forward at half power for one second
                self.logger.info("Moving forward at half power for one second.")
            elif self.sd.containsKey("turnCommand") and self.sd.getBoolean("turnCommand"):
                self.sd.putBoolean("turnCommand", False)
                Rotate(90.0).start()
                self.logger.info("Turning right 90 degrees.")

            # update navX status
            self.sd.putBoolean('navX/isConnected', navx.ahrs.isConnected())
            self.sd.putBoolean('navX/isCalibrating', navx.ahrs.isCalibrating())
            # self.sd.putNumber('navX/angle', self.navx.getAngle())
            self.sd.putNumber('navX/yaw', navx.ahrs.getFusedHeading())

            # update motor output statuses
            self.sd.putNumber("leftOutput", subsystems.motors.left_motor.getSetpoint())
            self.sd.putNumber("rightOutput", subsystems.motors.right_motor.getSetpoint())

            # update sonar readings
            self.sd.putNumber("sonar/front", sonar.front.get())
            self.sd.putNumber("sonar/frontRight", sonar.front_right.get())
            self.sd.putNumber("sonar/right", sonar.right.get())
            self.sd.putNumber("sonar/backRight", sonar.back_right.get())
            self.sd.putNumber("sonar/back", sonar.back.get())
            self.sd.putNumber("sonar/backLeft", sonar.back_left.get())
            self.sd.putNumber("sonar/left", sonar.left.get())
            self.sd.putNumber("sonar/frontLeft", sonar.front_left.get())
