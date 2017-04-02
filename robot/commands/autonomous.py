import logging

from wpilib.command.commandgroup import CommandGroup

from commands.controlgearmech import ControlGearMech
from commands.drivetorod import DriveToRod
from commands.rotate import Rotate
from commands.setspeed import SetSpeed


class AutonomousProgram(CommandGroup):
    def __init__(self, mode):
        super().__init__('Autonomous Program')
        self.logger = logging.getLogger("robot")

        if mode == "borkleft":  # just cross the base line
            self.addSequential(SetSpeed(0.2, 0.5))
            self.addSequential(Rotate(-20))
            self.addSequential(SetSpeed(0.2, 2.0))
        elif mode == "borkright":
            self.addSequential(SetSpeed(0.2, 0.5))
            self.addSequential(Rotate(20))
            self.addSequential(SetSpeed(0.2, 2.0))
        elif mode == "left":
            self.addSequential(SetSpeed(0.4, 0.3))
            self.addSequential(Rotate(-30))
            self.addSequential(SetSpeed(0.3, 0.8))
            self.addSequential(Rotate(38))
            self.addSequential(DriveToRod(timeout=3.5))
            self.addSequential(ControlGearMech(False))
            self.addSequential(SetSpeed(-0.1, 1.0))

            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(Rotate(-10))
            self.addSequential(SetSpeed(0.3, 1.0))
        elif mode == "right":
            self.addSequential(SetSpeed(0.4, 0.3))
            self.addSequential(Rotate(30))
            self.addSequential(SetSpeed(0.3, 0.8))
            self.addSequential(Rotate(-38))
            self.addSequential(DriveToRod(timeout=3.5))
            self.addSequential(ControlGearMech(False))
            self.addSequential(SetSpeed(-0.1, 1.0))

            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(Rotate(10))
            self.addSequential(SetSpeed(0.3, 1.0))
        else:
            self.addSequential(SetSpeed(0.3, 0.5))
            self.logger.info("Drive to rod now!")
            self.addSequential(DriveToRod(timeout=3.0))
            self.addSequential(ControlGearMech(False))
            self.addSequential(SetSpeed(-0.1, 1.0))
