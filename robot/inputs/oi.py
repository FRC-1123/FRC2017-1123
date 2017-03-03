import wpilib
from wpilib.buttons.joystickbutton import JoystickButton

import robotmap
from commands.switchcamera import SwitchCamera

joystick = None
controller = None


def init():
    """
    Initialize operator input (OI) objects.
    """

    global joystick, controller

    joystick = wpilib.Joystick(robotmap.joystick.port)
    controller = wpilib.XboxController(robotmap.joystick.port)

    start = JoystickButton(joystick, 7)
    start.whenPressed(SwitchCamera())
