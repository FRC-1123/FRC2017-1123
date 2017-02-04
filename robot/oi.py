import wpilib

import robotmap

joystick = None
controller = None


def init():
    """
    Initialize operator input (OI) objects.
    """

    global joystick, controller

    joystick = wpilib.Joystick(robotmap.joystick.port)
    # controller = wpilib.XboxController(robotmap.joystick.port)
