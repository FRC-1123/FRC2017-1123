from robotpy_ext.common_drivers.units import inch
from robotpy_ext.common_drivers.xl_max_sonar_ez import MaxSonarEZPulseWidth

import robotmap
from hrlv_max_sonar_ez import HRLVMaxSonarEZPulseWidth

front = None
back = None


def init():
    """
    Initialize sonar object.
    """
    global front, back

    front = HRLVMaxSonarEZPulseWidth(robotmap.sonar.front_channel, inch)
    back = MaxSonarEZPulseWidth(robotmap.sonar.back_channel, inch)
