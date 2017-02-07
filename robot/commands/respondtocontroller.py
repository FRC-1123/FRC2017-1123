import logging

from networktables import NetworkTables
from wpilib.command import Command

import subsystems
from inputs import oi

logging.basicConfig(level=logging.INFO)


class RespondToController(Command):
    """
    This command will respond to the controller's buttons.
    """

    def __init__(self):
        super().__init__("Respond to Controller")

        self.requires(subsystems.gear_mech)

        self.sd = NetworkTables.getTable("SmartDashboard")
        self.logger = logging.getLogger("robot")

    def execute(self):
        # for xbox controller

        # piston control
        if oi.controller.getAButton():  # piston out
            subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kForward)
            self.sd.putBoolean("pneumatic", True)
        elif oi.controller.getBButton():  # piston in
            subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kReverse)
            self.sd.putBoolean("pneumatic", False)

        # drive-to-rod control
            # if oi.controller.getStartButton():
            #     rod_pos = cameras.front_camera.get_rod_pos()
            #     if rod_pos is None:  # cannot find rod
            #         self.logger.critical("Couldn't find the rod!")
            #         RumbleController(1).start()
            #     else:
            #         self.logger.info("Driving to the rod!")
            #         DriveToRod().start()

                # for single joystick
        # if oi.joystick.getRawButton(robotmap.joystick.top_left_port):  # piston in
        #     subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kReverse)
        #     self.sd.putBoolean("pneumatic", False)
        # elif oi.joystick.getRawButton(robotmap.joystick.top_right_port):  # piston out
        #     subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kForward)
        #     self.sd.putBoolean("pneumatic", True)
