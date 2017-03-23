import logging

from networktables import NetworkTables
from wpilib.command import PIDCommand

import robotmap
import subsystems
from commands.followjoystick import FollowJoystick
from commands.rumblecontroller import RumbleController
from inputs import camera
from inputs import oi
from rectifieddrive import RectifiedDrive

logging.basicConfig(level=logging.DEBUG)


class LockOn(PIDCommand):
    '''
    This command dynamically transfers control between the driver and computer vision for driving to the rod
    '''

    def __init__(self):
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.sd.putBoolean("lockonRunning", True)

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

        # initialize PID controller with a period of 0.05 seconds
        super().__init__(kp, ki, kd, 0.05, kf, "Lock On")

        self.requires(subsystems.motors)

        turnController = self.getPIDController()
        turnController.setInputRange(-1.0, 1.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(ktolerance)
        turnController.setContinuous(True)
        turnController.setSetpoint(0.5)  # want rod to be at center

        self.drive = RectifiedDrive(30, 0.05)

        self.logger = logging.getLogger("robot")

        # self.is_autonomous = self.sd.getBoolean("isautonomous")
        self.is_lost = False  # can't find the rod

        # self.last_rod_pos = 0

    def returnPIDInput(self):
        rod_pos = camera.get_rod_pos()
        if rod_pos is None:
            self.logger.critical("Couldn't find the rod!")
            self.is_lost = True
            self.logger.critical("Returning control to the controller!")
            self.sd.putBoolean("lockonRunning", False)
            RumbleController(0.5).start()
            FollowJoystick().start()
            return 0.5
        else:
            self.last_rod_pos = rod_pos[0]
            self.sd.putNumber("rod/actual", rod_pos[0])
            return rod_pos[0]

    def usePIDOutput(self, output):
        power = oi.joystick.getRawAxis(robotmap.joystick.forwardAxis)  # get human command for steering and speed
        angular_vel = oi.joystick.getRawAxis(robotmap.joystick.steeringAxis)
        if self.is_lost or abs(angular_vel) >= 0.5:  # if we're lost or the human is insistent
            self.drive.rectified_drive(power, angular_vel)
        else:  # combine human and computer vision control
            self.drive.rectified_drive(power, -output * abs(0.5 - self.last_rod_pos) + (1.0 - abs(0.5 - self.last_rod_pos)) * angular_vel)

            # def isFinished(self):
            #     # timeout after 10 seconds or stop when within 8 inches of the wall
            #     if self.timeSinceInitialized() > self.timeout:
            #         return True
            #     sonar.update_readings()
            #     return sonar.distances[0] < 8.0
