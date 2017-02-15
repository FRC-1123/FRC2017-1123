from robotpy_ext.common_drivers.units import meter
from robotpy_ext.common_drivers.xl_max_sonar_ez import MaxSonarEZPulseWidth

import robotmap

front = None


def init():
    """
    Initialize sonar object.
    """
    global front

    front = MaxSonarEZPulseWidth(robotmap.sonar.front_channel, meter)
