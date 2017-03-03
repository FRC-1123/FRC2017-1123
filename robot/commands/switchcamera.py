import wpilib
from wpilib.command import InstantCommand
from networktables import NetworkTables
import logging

import subsystems


class SwitchCamera(InstantCommand):
    """
    This command rumbles the Xbox controller for a set amount of time.
    """

    def __init__(self):
        super().__init__("Switch Camera")

        sd = NetworkTables.getTable("SmartDashboard")
        cur_direct = sd.getNumber("direction")


        if cur_direct == 1:
            subsystems.motors.reverseDirection()
        else:
            subsystems.motors.forwardDirection()
        sd.putNumber("direction", -cur_direct)

        logger = logging.getLogger("robot")
        logger.info("switched camera")
