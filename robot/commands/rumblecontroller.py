import wpilib
from wpilib.command import TimedCommand

import oi


class RumbleController(TimedCommand):
    """
    This command rumbles the Xbox controller for a set amount of time.
    """

    def __init__(self, duration):
        super().__init__("Rumble controller", duration)

        oi.controller.setRumble(wpilib.GenericHID.RumbleType.kRightRumble, True)

    def end(self):
        oi.controller.setRumble(wpilib.GenericHID.RumbleType.kRightRumble, False)
