import logging

from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand

from commands.controldumper import ControlDumper
from commands.drivetorod import DriveToRod
from commands.finishautonomous import FinishAutonomous
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
            self.addSequential(SetSpeed(0.3, 0.7))
            self.addSequential(Rotate(80))
            self.addSequential(DriveToRod(timeout=4.0))
            self.addSequential(FinishAutonomous("left"))
        elif mode == "right":
            self.addSequential(SetSpeed(0.4, 0.3))
            self.addSequential(Rotate(30))
            self.addSequential(SetSpeed(0.3, 0.7))
            self.addSequential(Rotate(-80))
            self.addSequential(DriveToRod(timeout=4.0))
            self.addSequential(FinishAutonomous("right"))
        elif mode == "angledleft":
            self.addSequential(SetSpeed(0.3, 0.8))
            self.addSequential(Rotate(38))
            self.addSequential(DriveToRod(timeout=3.5))
            self.addSequential(WaitCommand(0.5))
            self.addSequential(SetSpeed(-0.1, 1.0))

            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(Rotate(-20))
            self.addSequential(SetSpeed(0.3, 1.0))
        elif mode == "angledright":
            self.addSequential(SetSpeed(0.3, 0.8))
            self.addSequential(Rotate(-38))
            self.addSequential(DriveToRod(timeout=3.5))
            self.addSequential(WaitCommand(0.5))
            self.addSequential(SetSpeed(-0.1, 1.0))

            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(Rotate(20))
            self.addSequential(SetSpeed(0.3, 1.0))
        elif mode == "boilerleft":
            self.addSequential(SetSpeed(0.3, 0.35))
            self.addSequential(ControlDumper(False))
            self.addSequential(WaitCommand(2.0))

            self.addParallel(ControlDumper(True))
            self.addSequential(Rotate(45))
            self.addSequential(SetSpeed(0.3, 0.3))
            self.addSequential(Rotate(90))
            self.addSequential(DriveToRod(timeout=3.5))
            self.addSequential(FinishAutonomous("left"))
        elif mode == "boilerright":
            self.addSequential(SetSpeed(-0.3, 0.4))
            self.addParallel(ControlDumper(False))
            self.addSequential(WaitCommand(2.0))

            self.addParallel(ControlDumper(True))
            self.addSequential(Rotate(-45))
            self.addSequential(SetSpeed(-0.3, 0.3))
            self.addSequential(Rotate(135))
            self.addSequential(DriveToRod(timeout=3.5))
            self.addSequential(FinishAutonomous("right"))
        elif mode == "oldleft":
            self.addSequential(SetSpeed(0.2, 0.5))
            self.addSequential(Rotate(-30))
            self.addSequential(SetSpeed(0.2, 1.2))
            self.addSequential(Rotate(40))
            self.addSequential(DriveToRod(timeout=3.5))
            self.addSequential(WaitCommand(0.5))
            self.addSequential(SetSpeed(-0.1, 1.0))

            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(Rotate(-20))
            self.addSequential(SetSpeed(0.3, 1.0))
        elif mode == "oldright":
            self.addSequential(SetSpeed(0.2, 0.5))
            self.addSequential(Rotate(30))
            self.addSequential(SetSpeed(0.2, 1.2))
            self.addSequential(Rotate(-40))
            self.addSequential(DriveToRod(timeout=3.5))
            self.addSequential(WaitCommand(0.5))
            self.addSequential(SetSpeed(-0.1, 1.0))

            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(Rotate(20))
            self.addSequential(SetSpeed(0.3, 1.0))
        else:  # center mode
            # self.addSequential(SetSpeed(0.3, 0.3))
            self.logger.info("Drive to rod now!")
            self.addSequential(DriveToRod(timeout=4.0))
            self.addSequential(FinishAutonomous("center"))
