import wpilib
from wpilib.command import Command

import subsystems
import robotmap
from networktables import NetworkTables


class FollowJoystick(Command):
    '''
    This command will read the joystick's y axis and use that value to control
    the speed of the SingleMotor subsystem.
    '''

    def __init__(self):
        super().__init__('Follow Joystick')

        self.requires(subsystems.motors)
        self.requires(subsystems.oi)

        self.sd = NetworkTables.getTable("SmartDashboard")
        self.forward_timer = wpilib.Timer()
        self.forward_timer.start()
        self.init_forward = False  # only needed the first time forward command is sent because forward_timer starts at 0

    def execute(self):
        if self.sd.containsKey("forwardCommand") and self.sd.getBoolean(
                "forwardCommand"):  # check if move forward button pressed
            self.sd.putBoolean("forwardCommand", False)
            self.forward_timer.reset()
            self.init_forward = True
        if self.init_forward and self.forward_timer.get() < 1:  # check if move forward command sent within 1 second
            subsystems.motors.setSpeed(.5)
        else:
            subsystems.motors.robot_drive.tankDrive(subsystems.oi.joystick, robotmap.joystick.left_port,
                                                subsystems.oi.joystick, robotmap.joystick.right_port, True)

