import logging

import wpilib
from networktables import NetworkTables
from wpilib.command import Command

import navx
import subsystems
from commands.rotate import Rotate
from commands.setspeed import SetSpeed

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

        # put initial tape contour detection hsv range
        # self.sd.putNumber("camera/minh", subsystems.front_camera.min_h)
        # self.sd.putNumber("camera/mins", subsystems.front_camera.min_s)
        # self.sd.putNumber("camera/minv", subsystems.front_camera.min_v)
        # self.sd.putNumber("camera/maxh", subsystems.front_camera.max_h)
        # self.sd.putNumber("camera/maxs", subsystems.front_camera.max_s)
        # self.sd.putNumber("camera/maxv", subsystems.front_camera.max_v)

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

            # update tape contour detection hsv range
            # if self.sd.containsKey("camera/minh"):
            #     subsystems.front_camera.min_h = self.sd.getNumber("camera/minh")
            # if self.sd.containsKey("camera/mins"):
            #     subsystems.front_camera.min_s = self.sd.getNumber("camera/mins")
            # if self.sd.containsKey("camera/minv"):
            #     subsystems.front_camera.min_v = self.sd.getNumber("camera/minv")
            # if self.sd.containsKey("camera/maxh"):
            #     subsystems.front_camera.max_h = self.sd.getNumber("camera/maxh")
            # if self.sd.containsKey("camera/maxs"):
            #     subsystems.front_camera.max_s = self.sd.getNumber("camera/maxs")
            # if self.sd.containsKey("camera/maxv"):
            #     subsystems.front_camera.max_v = self.sd.getNumber("camera/maxv")

            # update navX status
            self.sd.putBoolean('navX/isConnected', navx.ahrs.isConnected())
            self.sd.putBoolean('navX/isCalibrating', navx.ahrs.isCalibrating())
            # self.sd.putNumber('navX/angle', self.navx.getAngle())
            self.sd.putNumber('navX/yaw', navx.ahrs.getFusedHeading())

            # update motor output statuses
            self.sd.putNumber("leftOutput", subsystems.motors.left_motor.getSetpoint())
            self.sd.putNumber("rightOutput", subsystems.motors.right_motor.getSetpoint())
