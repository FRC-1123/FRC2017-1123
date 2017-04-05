import logging

from wpilib.command import InstantCommand

import subsystems

logging.basicConfig(level=logging.INFO)


class ControlDumper(InstantCommand):
    """
    This command opens and closes the ball dumper.
    """

    def __init__(self, closed):
        super().__init__("Control Dumper")

        self.requires(subsystems.dumper)

        self.closed = closed

    def initialize(self):
        logger = logging.getLogger("robot")

        if self.closed:
            subsystems.dumper.double_solenoid.set(subsystems.dumper.double_solenoid.Value.kReverse)
            logger.info("dumper closed")
        else:
            subsystems.dumper.double_solenoid.set(subsystems.dumper.double_solenoid.Value.kForward)
            logger.info("dumper open")
