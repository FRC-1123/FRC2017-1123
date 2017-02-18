from robotpy_ext.common_drivers.units import inch
from robotpy_ext.common_drivers.xl_max_sonar_ez import MaxSonarEZPulseWidth
from wpilib import DigitalOutput

import robotmap
from hrlv_max_sonar_ez import HRLVMaxSonarEZPulseWidth

front = None
front_right = None
right = None
back_right = None
back = None
back_left = None
left = None
front_left = None

pinger = None


def init():
    """
    Initialize sonar object.
    """
    global front, front_right, right, back_right, back, back_left, left, front_left, pinger

    front = MaxSonarEZPulseWidth(robotmap.sonar.front_channel, inch)
    front_right = MaxSonarEZPulseWidth(robotmap.sonar.front_right_channel, inch)
    right = MaxSonarEZPulseWidth(robotmap.sonar.right_channel, inch)
    back_right = MaxSonarEZPulseWidth(robotmap.sonar.back_right_channel, inch)
    back = HRLVMaxSonarEZPulseWidth(robotmap.sonar.back_channel, inch)
    back_left = MaxSonarEZPulseWidth(robotmap.sonar.back_left_channel, inch)
    left = MaxSonarEZPulseWidth(robotmap.sonar.left_channel, inch)
    front_left = MaxSonarEZPulseWidth(robotmap.sonar.front_left_channel, inch)

    pinger = DigitalOutput(robotmap.sonar.pinger_channel)


def update_readings():
    if pinger is not None:
        pinger.pulse(0.0001)  # pulse for 100 microseconds
