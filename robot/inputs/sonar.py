from robotpy_ext.common_drivers.units import meter
from robotpy_ext.common_drivers.xl_max_sonar_ez import MaxSonarEZPulseWidth

import robotmap

sonar = None


def init():
    """
    Initialize sonar object.
    """
    global sonar

    sonar = MaxSonarEZPulseWidth(robotmap.sonar.channel, meter)
