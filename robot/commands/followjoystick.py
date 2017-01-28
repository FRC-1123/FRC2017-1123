import logging

import robotmap
import subsystems
import wpilib
from networktables import NetworkTables
from wpilib.command import Command

logging.basicConfig(level=logging.DEBUG)


class FollowJoystick(Command):
    '''
    This command will read the joystick's y axis and use that value to control
    the speed of the SingleMotor subsystem.
    '''

    def __init__(self):
        super().__init__('Follow Joystick')

        self.requires(subsystems.motors)
        self.requires(subsystems.oi)
        self.requires(subsystems.gear_mech)

        self.sd = NetworkTables.getTable("SmartDashboard")
        self.forward_timer = wpilib.Timer()
        self.forward_timer.start()
        self.nt_timer = wpilib.Timer()  # timer for updating NetworkTables
        self.nt_timer.start()
        self.init_forward = False  # only needed the first time forward command is sent because forward_timer starts at 0

    def execute(self):
        if self.sd.containsKey("forwardCommand") and self.sd.getBoolean(
                "forwardCommand"):  # check if move forward button pressed
            self.sd.putBoolean("forwardCommand", False)
            self.forward_timer.reset()
            self.init_forward = True
        if self.init_forward and self.forward_timer.get() < 1:  # check if move forward command sent within 1 second
            subsystems.motors.setSpeed(.2)
        else:
            subsystems.motors.robot_drive.tankDrive(subsystems.oi.joystick, robotmap.joystick.left_port,
                                                    subsystems.oi.joystick, robotmap.joystick.right_port, True)

        if self.nt_time.hasPeriodPassed(.2):  # update NetworkTables every 0.2 seconds
            
            # update pneumatics status
            if subsystems.oi.controller.getAButton():  # piston out
                subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.kForward)
                self.sd.putBoolean("pneumatic", True)
            elif subsystems.oi.controller.getBButton():  # piston in
                subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.kReverse)
                self.sd.putBoolean("pneumatic", False)

            # update motor output statuses
            self.sd.putNumber("leftOutput", subsystems.motors.left_motor.getSetpoint())
            self.sd.putNumber("rightOutput", subsystems.motors.right_motor.getSetpoint())

