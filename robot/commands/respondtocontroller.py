from networktables import NetworkTables
from wpilib.command import Command

import robotmap
import subsystems
from inputs import oi


class RespondToController(Command):
    """
    This command will respond to the controller's buttons.
    """

    def __init__(self):
        super().__init__("Respond to Controller")

        self.requires(subsystems.gear_mech)

        self.sd = NetworkTables.getTable("SmartDashboard")

    def execute(self):
        # for xbox controller
        # if oi.controller.getAButton():  # piston out
        #     subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kForward)
        #     self.sd.putBoolean("pneumatic", True)
        # elif oi.controller.getBButton():  # piston in
        #     subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kReverse)
        #     self.sd.putBoolean("pneumatic", False)
        #     # if oi.controller.getXButton():  # turn 90 degrees left
        #     #     Rotate(-90.0).start()
        #     # elif oi.controller.getYButton():  # turn 90 degrees right
        #     #     Rotate(90.0).start()

        # for arcade drive
        if oi.joystick.getRawButton(robotmap.joystick.top_left_port):  # piston in
            subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kReverse)
            self.sd.putBoolean("pneumatic", False)
        elif oi.joystick.getRawButton(robotmap.joystick.top_right_port):  # piston out
            subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kForward)
            self.sd.putBoolean("pneumatic", True)
