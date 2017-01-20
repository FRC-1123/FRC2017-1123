#!/usr/bin/env python3

import wpilib
from networktables import NetworkTables

from commandbased import CommandBasedRobot
import subsystems
from commands.autonomous import AutonomousProgram
from commands.setspeed import SetSpeed

import logging

logging.basicConfig(level=logging.DEBUG)


class Robot(CommandBasedRobot):
    '''
    The CommandBasedRobot base class implements almost everything you need for
    a working robot program. All you need to do is set up the subsystems and
    commands. You do not need to override the "periodic" functions, as they
    will automatically call the scheduler. You may override the "init" functions
    if you want to do anything special when the mode changes.
    '''

    def robotInit(self):
        '''
        This is a good place to set up your subsystems and anything else that
        you will need to access later.
        '''
        self.sd = NetworkTables.getTable("SmartDashboard")

        subsystems.init()
        self.autonomousProgram = AutonomousProgram()

    def robotPeriodic(self):
        self.sd.putNumber("leftOutput", subsystems.motors.left_motor.getSetpoint())
        self.sd.putNumber("rightOutput", subsystems.motors.right_motor.getSetpoint())

    def autonomousInit(self):
        '''
        You should call start on your autonomous program here. You can
        instantiate the program here if you like, or in robotInit as in this
        example. You can also use a SendableChooser to have the autonomous
        program chosen from the SmartDashboard.
        '''
        self.autonomousProgram.start()

    def teleopInit(self):
        self.sd.putBoolean("timeRunning", True)

    def testPeriodic(self):
        # this is just proof-of-concept code, should really be in a subsystem
        if self.sd.containsKey("forwardCommand") and self.sd.getBoolean(
                "forwardCommand"):  # check if move forward button pressed
            self.sd.putBoolean("forwardCommand", False)
            SetSpeed(power=.5, timeoutInSeconds=1)


if __name__ == '__main__':
    wpilib.run(Robot)
