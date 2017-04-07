import logging

from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand

from commands.controldumper import ControlDumper
from commands.drivetorod import DriveToRod
from commands.rotate import Rotate
from commands.setspeed import SetSpeed

from inputs import switches


class FinishAutonomous(CommandGroup):
    def __init__(self, mode):
        super().__init__('Finish Autonomous')
        self.logger = logging.getLogger("robot")

        if switches.gear_mech_switch.get():  # don't do anything if switch not pressed
            return

        self.addSequential(WaitCommand(0.5))
        if mode == "left":
            self.addSequential(SetSpeed(-0.1, 1.0))
            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(Rotate(-45))
            self.addSequential(SetSpeed(0.3, 1.0))
            self.addSequential(Rotate(90))
        elif mode == "right":
            self.addSequential(SetSpeed(-0.1, 1.0))
            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(Rotate(45))
            self.addSequential(SetSpeed(0.3, 1.0))
            self.addSequential(Rotate(-90))
        else:
            self.addSequential(SetSpeed(-0.1, 1.0))
            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(WaitCommand(5.0))
            self.addSequential(SetSpeed(0.3, 0.8))
