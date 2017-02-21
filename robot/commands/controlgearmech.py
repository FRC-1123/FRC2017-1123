import logging

from networktables import NetworkTables
from wpilib.command import InstantCommand

import subsystems

logging.basicConfig(level=logging.INFO)


class ControlGearMech(InstantCommand):
    """
    This command opens and closes the gear mechanism.
    """

    def __init__(self, closed):
        super().__init__("Control Gear Mechanism")

        self.requires(subsystems.gear_mech)

        sd = NetworkTables.getTable("SmartDashboard")

        if closed:
            subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kReverse)
            sd.putBoolean("pneumatic", False)
        else:
            subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kForward)
            sd.putBoolean("pneumatic", True)
