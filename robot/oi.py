import wpilib
import robotmap


joystick = None
controller = None

def init():
    '''
    Assign commands to button actions, and publish your joysticks so you
    can read values from them later.
    '''

    global joystick, controller

    joystick = wpilib.Joystick(robotmap.joystick.port)
    controller = wpilib.XboxController(robotmap.joystick.port)


    # trigger = JoystickButton(self.joystick, Joystick.ButtonType.kTrigger)
    # trigger.whenPressed(Crash())
