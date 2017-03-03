import wpilib
from wpilib.buttons.joystickbutton import JoystickButton

import robotmap

joystick = None
controller = None
start_btn = None


def init():
    """
    Initialize operator input (OI) objects.
    """

    global joystick, controller, start_btn

    joystick = wpilib.Joystick(robotmap.joystick.port)
    controller = wpilib.XboxController(robotmap.joystick.port)

    start_btn = JoystickButton(joystick, 7)
