import logging

from networktables import NetworkTables
from wpilib.command import InstantCommand

import subsystems


class SwitchCamera(InstantCommand):

    def __init__(self):
        super().__init__("Switch Camera")

    def initialize(self):
        sd = NetworkTables.getTable("SmartDashboard")
        cur_direct = sd.getNumber("direction")

        if cur_direct == 1:
            subsystems.motors.reverseDirection()
        else:
            subsystems.motors.forwardDirection()

        logger = logging.getLogger("robot")
        logger.info("Switched camera")
