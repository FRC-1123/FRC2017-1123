import wpilib
from networktables import NetworkTables
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

        self.sd = NetworkTables.getTable("SmartDashboard")

        self.timer = wpilib.Timer()
        self.timer.start()

    def execute(self):
        if self.timer.hasPeriodPassed(0.05):
            # subsystems.climbing_mech.setSpeed(oi.controller.getRawAxis(3))
            # if oi.controller.getYButton():  # climb down
            #     subsystems.climbing_mech.setSpeed(-0.3)
            if oi.controller.getXButton():  # climb up
                subsystems.climbing_mech.setSpeed(1.0)
            elif self.sd.containsKey("climbDownCommand") and self.sd.getBoolean("climbDownCommand"):
                subsystems.climbing_mech.setSpeed(-0.2)
            else:
                subsystems.climbing_mech.setSpeed(0)

    def end(self):
        # set output to 0 on end
        subsystems.climbing_mech.setSpeed(0)
