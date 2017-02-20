import wpilib
from wpilib.command import Command

import subsystems
from inputs import oi


class ListenForClimb(Command):
    """
    Control the winch through the X and Y buttons.
    """

    def __init__(self):
        super().__init__('Listen for climb')

        self.requires(subsystems.climbing_mech)

        self.timer = wpilib.Timer()
        self.timer.start()

    def execute(self):
        if self.timer.hasPeriodPassed(0.05):
            if oi.controller.getYButton():  # climb up
                subsystems.climbing_mech.setSpeed(1)
            elif oi.controller.getXButton():  # climb down
                subsystems.climbing_mech.setSpeed(-0.3)
            else:
                subsystems.climbing_mech.setSpeed(0)

    def end(self):
        # set output to 0 on end
        subsystems.climbing_mech.setSpeed(0)
