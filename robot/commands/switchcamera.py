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
        logger = logging.getLogger("robot")

        if cur_direct == 1:
            subsystems.motors.reverseDirection()
            logger.info("Reversed")
        else:
            subsystems.motors.forwardDirection()
            logger.info("Forward")

        logger.info("Switched camera")
