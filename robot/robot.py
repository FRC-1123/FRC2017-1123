#!/usr/bin/env python3

import logging

import wpilib
from commandbased import CommandBasedRobot
from networktables import NetworkTables

import subsystems
from commands.autonomous import AutonomousProgram
from commands.updatenetworktables import UpdateNetworkTables

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
        self.updateNT = UpdateNetworkTables()

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
        self.updateNT.start()


if __name__ == '__main__':
    wpilib.run(Robot)
