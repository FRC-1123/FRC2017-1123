#!/usr/bin/env python3

import wpilib
import ctre
from networktables import NetworkTables
import time

# Logging to see messages from networktables
import logging
logging.basicConfig(level=logging.DEBUG)



class Robot(wpilib.IterativeRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        left_motor = ctre.CANTalon(0)
        right_motor = ctre.CANTalon(1)
        self.robot_drive = wpilib.RobotDrive(left_motor, right_motor)
        self.robot_drive.setMaxOutput(2)

        self.stick = wpilib.Joystick(0)
        self.controller = wpilib.XboxController(0)

        sd = NetworkTables.getTable("SmartDashboard")
        
        self.timer = wpilib.Timer()
        self.timer.start()

        sd.putBoolean("timeRunning", True)


    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.auto_loop_counter = 0

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        # Check if we've completed 100 loops (approximately 2 seconds)
        if self.auto_loop_counter < 100:
            self.robot_drive.drive(-0.5, 0)  # Drive forwards at half speed
            self.auto_loop_counter += 1
        else:
            self.robot_drive.drive(0, 0)  # Stop robot

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.robot_drive.tankDrive(self.stick, 5, self.stick, 1, True)  # 5 and 1 are left and right joystick axes, respectively
        if self.controller.getAButton():
            self.robot_drive.drive(-.5, 0)  # move forward slowly
        if self.controller.getXButton():  # turn in place
            self.robot_drive.setLeftRightMotorOutputs(-.5, .5)
        elif self.controller.getYButton():  # turn in place
            self.robot_drive.setLeftRightMotorOutputs(.5, -.5)
        
        # interact with NetworkTables
        if timer.hasPeriodPassed(1):
            try:
                print("dsTime:", sd.getNumber("dsTime"))
            except KeyError:
                print("dsTime: N/A")
            sd.putNumber("robotTime", timer.get())
        

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()


if __name__ == "__main__":
    wpilib.run(Robot)
