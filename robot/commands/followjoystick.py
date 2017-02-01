import logging

from networktables import NetworkTables
from wpilib.command import Command

import oi
import robotmap
import subsystems

logging.basicConfig(level=logging.DEBUG)


class FollowJoystick(Command):
    """
    This command will read the joysticks' y-axes and uses tank drive.
    """

    def __init__(self):
        super().__init__('Follow Joystick')

        self.requires(subsystems.motors)
        self.requires(subsystems.gear_mech)

        self.sd = NetworkTables.getTable("SmartDashboard")

    def execute(self):
        # tank drive
        subsystems.motors.robot_drive.tankDrive(oi.joystick, robotmap.joystick.left_port, oi.joystick, robotmap.joystick.right_port, True)

        # respond to buttons
        if oi.controller.getAButton():  # piston out
            subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kForward)
            self.sd.putBoolean("pneumatic", True)
        elif oi.controller.getBButton():  # piston in
            subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kReverse)
            self.sd.putBoolean("pneumatic", False)
            # if oi.controller.getXButton():  # turn 90 degrees left
            #     Rotate(-90.0).start()
            # elif oi.controller.getYButton():  # turn 90 degrees right
            #     Rotate(90.0).start()
