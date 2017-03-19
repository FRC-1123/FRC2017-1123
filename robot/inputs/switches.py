from wpilib import DigitalInput

import robotmap

gear_mech_switch = None


def init():
    """
    Initialize switch objects.
    """
    global gear_mech_switch

    gear_mech_switch = DigitalInput(robotmap.switches.climb_switch_channel)
