from robotpy_ext.common_drivers.units import inch
from robotpy_ext.common_drivers.xl_max_sonar_ez import MaxSonarEZPulseWidth

import robotmap
from hrlv_max_sonar_ez import HRLVMaxSonarEZPulseWidth

front = None
front_right = None
back = None


def init():
    """
    Initialize sonar object.
    """
    global front, front_right, back

    front = MaxSonarEZPulseWidth(robotmap.sonar.front_channel, inch)
    front_right = MaxSonarEZPulseWidth(robotmap.sonar.front_right_channel, inch)
    back = HRLVMaxSonarEZPulseWidth(robotmap.sonar.back_channel, inch)
