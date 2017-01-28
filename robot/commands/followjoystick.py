import logging

import wpilib
from networktables import NetworkTables
from robotpy_ext.common_drivers import navx
from wpilib.command import Command

import robotmap
import subsystems

import rotate

logging.basicConfig(level=logging.DEBUG)


class FollowJoystick(Command):
    '''
    This command will read the joysticks' y-axes and uses tank drive.
    '''

    def __init__(self):
        super().__init__('Follow Joystick')

        self.requires(subsystems.motors)
        self.requires(subsystems.oi)
        
        self.sd = NetworkTables.getTable("SmartDashboard")

    def execute(self):
        subsystems.motors.robot_drive.tankDrive(subsystems.oi.joystick, robotmap.joystick.left_port, subsystems.oi.joystick,
                                                robotmap.joystick.right_port, True)
        # respond to buttons
        if subsystems.oi.controller.getAButton():  # piston out
            subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.kForward)
            self.sd.putBoolean("pneumatic", True)
        elif subsystems.oi.controller.getBButton():  # piston in
            subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.kReverse)
            self.sd.putBoolean("pneumatic", False)
        if subsystems.oi.controller.getXButton():  # turn 90 degrees left
            rotate.Rotate(-90.0).start()
        elif subsystems.oi.controller.getYButton():  # turn 90 degrees right
            rotate.Rotate(90.0).start()
