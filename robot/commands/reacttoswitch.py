import wpilib
from wpilib.command import Command

import subsystems
from commands.setspeed import SetSpeed


# FIXME: See fixme in switches subsystem
class ReactToSwitch(Command):
    """
    This command drives the robot backwards when the switch is pressed.
    """

    def __init__(self):
        super().__init__('React to Switch')

        self.requires(subsystems.switches)
        self.requires(subsystems.motors)

        self.timer = wpilib.Timer()  # timer for checking the switches' states
        self.timer.start()

    def execute(self):
        # drive the robot backwards at half power for one second when the limit switch is pressed
        if self.timer.hasPeriodPassed(0.2) and subsystems.switches.limit_switch.get():
            SetSpeed(0.5, 1).start()
