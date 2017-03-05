from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand

from commands.controlgearmech import ControlGearMech
from commands.drivetorod import DriveToRod
from commands.rotate import Rotate
from commands.setspeed import SetSpeed


class AutonomousProgram(CommandGroup):
    def __init__(self, mode):
        super().__init__('Autonomous Program')

        if mode == "left":
            self.addSequential(ControlGearMech(True))
            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(Rotate(-20))
            self.addSequential(SetSpeed(-0.3, 2.4))
            self.addSequential(Rotate(30))
            self.addSequential(DriveToRod(timeout=3))
            self.addSequential(ControlGearMech(False))
            self.addSequential(WaitCommand(7))
            # self.addSequential(SetSpeed(0.3, 1))
            self.addParallel(ControlGearMech(True))
            # self.addSequential(Rotate(-10))
            # self.addSequential(SetSpeed(-0.5, 2))
        elif mode == "right":
            self.addSequential(ControlGearMech(True))
            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(Rotate(20))
            self.addSequential(SetSpeed(-0.3, 2.4))
            self.addSequential(Rotate(-30))
            self.addSequential(DriveToRod(timeout=3))
            self.addSequential(ControlGearMech(False))
            self.addSequential(WaitCommand(7))
            # self.addSequential(SetSpeed(0.3, 1))
            self.addParallel(ControlGearMech(True))
            # self.addSequential(Rotate(10))
            # self.addSequential(SetSpeed(-0.5, 2))
        else:
            self.addSequential(ControlGearMech(True))
            self.addSequential(SetSpeed(-0.3, 1.5))
            self.addSequential(DriveToRod(timeout=5))
            self.addSequential(ControlGearMech(False))
            self.addSequential(WaitCommand(7))
            # self.addSequential(SetSpeed(0.3, 1))
            self.addParallel(ControlGearMech(True))
            # self.addSequential(Rotate(80))
            # self.addSequential(SetSpeed(-0.5, 1))
            # self.addSequential(Rotate(-80))
            # self.addSequential(SetSpeed(-0.5, 2))
