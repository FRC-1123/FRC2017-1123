import logging

import wpilib
from networktables import NetworkTables
from wpilib.command import Command

import subsystems
from commands.rotate import Rotate
from commands.setspeed import SetSpeed
from commands.switchcamera import SwitchCamera
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
        if self.nt_timer.hasPeriodPassed(0.1):  # update NetworkTables every 0.1 seconds
            # dashboard forward button (for demonstration purposes)
            if self.sd.containsKey("forwardCommand") and self.sd.getBoolean("forwardCommand"):  # check if move forward button pressed
                self.sd.putBoolean("forwardCommand", False)
                SetSpeed(-0.5, 1).start()  # move forward at half power for one second
                self.logger.info("Moving forward at half power for one second.")
            elif self.sd.containsKey("turnCommand") and self.sd.getBoolean("turnCommand"):
                self.sd.putBoolean("turnCommand", False)
                Rotate(90.0).start()
                self.logger.info("Turning right 90 degrees.")
            if self.sd.containsKey("switchAllCommand") and self.sd.getBoolean("switchAllCommand"):
                self.sd.putBoolean("switchAllCommand", False)
                SwitchCamera().start()
                self.logger.info("Reversed everything.")

            # update navX status
            self.sd.putBoolean('navX/isConnected', navx.ahrs.isConnected())
            self.sd.putBoolean('navX/isCalibrating', navx.ahrs.isCalibrating())
            # self.sd.putNumber('navX/angle', self.navx.getAngle())
            self.sd.putNumber('navX/yaw', navx.ahrs.getFusedHeading())

            # update motor output statuses
            self.sd.putNumber("leftOutput", subsystems.motors.left_motor.getSetpoint())
            self.sd.putNumber("rightOutput", subsystems.motors.right_motor.getSetpoint())
            self.sd.putNumber("leftCurrent", subsystems.motors.left_motor.getOutputCurrent())
            self.sd.putNumber("rightCurrent", subsystems.motors.right_motor.getOutputCurrent())

            # with open("outputs.txt", "a") as outfile:
            #     outfile.write("{}\t{}\n".format(subsystems.motors.left_motor.getOutputCurrent(), subsystems.motors.right_motor.getOutputCurrent()))

            # update sonar readings
            sonar.update_readings()
            self.sd.putNumber("sonar/front", sonar.distances[0])
            self.sd.putNumber("sonar/frontRight", sonar.distances[1])
            self.sd.putNumber("sonar/right", sonar.distances[2])
            self.sd.putNumber("sonar/backRight", sonar.distances[3])
            self.sd.putNumber("sonar/back", sonar.distances[4])
            self.sd.putNumber("sonar/backLeft", sonar.distances[5])
            self.sd.putNumber("sonar/left", sonar.distances[6])
            self.sd.putNumber("sonar/frontLeft", sonar.distances[7])

            self.sd.putNumber("sonar/front_speed", sonar.speeds[0])
            self.sd.putNumber("sonar/frontRight_speed", sonar.speeds[1])
            self.sd.putNumber("sonar/right_speed", sonar.speeds[2])
            self.sd.putNumber("sonar/backRight_speed", sonar.speeds[3])
            self.sd.putNumber("sonar/back_speed", sonar.speeds[4])
            self.sd.putNumber("sonar/backLeft_speed", sonar.speeds[5])
            self.sd.putNumber("sonar/left_speed", sonar.speeds[6])
            self.sd.putNumber("sonar/frontLeft_speed", sonar.speeds[7])
