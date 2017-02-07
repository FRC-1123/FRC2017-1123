from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand

from commands.rotate import Rotate
from commands.setspeed import SetSpeed


class AutonomousProgram(CommandGroup):
    def __init__(self, mode):
        super().__init__('Autonomous Program')

        if mode == "left":
            self.addSequential(Rotate(90))
            self.addSequential(WaitCommand(timeout=1))
            self.addSequential(SetSpeed(power=-0.7, timeoutInSeconds=1))
        elif mode == "right":
            self.addSequential(Rotate(-90))
            self.addSequential(WaitCommand(timeout=1))
            self.addSequential(SetSpeed(power=-0.7, timeoutInSeconds=1))
        else:
            self.addSequential(SetSpeed(power=-0.7, timeoutInSeconds=1))
