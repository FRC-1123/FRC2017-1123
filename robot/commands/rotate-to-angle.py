import logging

from networktables import NetworkTables
from wpilib.command import PIDCommand

import oi
import robotmap
import subsystems

logging.basicConfig(level=logging.DEBUG)


class FollowJoystick(PIDCommand):
    """
    This command will read the joysticks' y-axes and uses arcade drive.
    It corrects for perturbations using the NavX.
    """

    def __init__(self):
        # PID constants
        kp = 0.03
        ki = 0.00
        kd = 0.00
        kf = 0.00
        ktolerance = 2.0  # tolerance of 2 degrees

        # initialize PID controller with a period of 0.05 seconds
        super().__init__(kp, ki, kd, 0.05, kf, "Rotate to angle {}".format(angle))

        self.requires(subsystems.motors)

        self.rate = 1.0

        turnController = self.getPIDController()
        turnController.setInputRange(-180.0, 180.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(ktolerance)
        turnController.setContinuous(True)


    def operatorControl(self):
        

        while self.isOperatorControl() and self.isEnabled():
            
            if tm.hasPeriodPassed(1.0):
                print("NavX Gyro", self.ahrs.getYaw(), self.ahrs.getAngle())
            
            rotateToAngle = False
            if self.stick.getRawButton(1):
                self.ahrs.reset()
            
            if self.stick.getRawButton(2):
                self.turnController.setSetpoint(0.0)
                rotateToAngle = True
            elif self.stick.getRawButton(3):
                self.turnController.setSetpoint(90.0)
                rotateToAngle = True
            elif self.stick.getRawButton(4):
                self.turnController.setSetpoint(179.9)
                rotateToAngle = True
            elif self.stick.getRawButton(5):
                self.turnController.setSetpoint(-90.0)
                rotateToAngle = True
            
            if rotateToAngle:
                self.turnController.enable()
                currentRotationRate = self.rotateToAngleRate
            else:
                self.turnController.disable()
                currentRotationRate = self.stick.getX()
            
            # Use the joystick Y axis for forward movement,
            # and either the X axis for rotation or the current
            # calculated rotation rate depending upon whether
            # "rotate to angle" is active.
            #
            # This works better for mecanum drive robots, but this 
            # illustrates one way you could implement this using
            # a 4 wheel drive robot
            
            self.myRobot.arcadeDrive(self.stick.getY(), currentRotationRate)
            
            wpilib.Timer.delay(0.005) # wait for a motor update time
        
    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        self.rotateToAngleRate = output
