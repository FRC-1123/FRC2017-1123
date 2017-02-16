from wpilib.command.commandgroup import CommandGroup

from commands.drivetorod import DriveToRod
from commands.rotate import Rotate
from commands.setspeed import SetSpeed


class AutonomousProgram(CommandGroup):
    def __init__(self, mode):
        super().__init__('Autonomous Program')

        if mode == "left":
            self.addSequential(SetSpeed(0.3, 1))
            self.addSequential(Rotate(30))
            self.addSequential(DriveToRod())
        elif mode == "right":
            self.addSequential(SetSpeed(0.3, 1))
            self.addSequential(Rotate(-30))
            self.addSequential(DriveToRod())
        else:
            self.addSequential(DriveToRod())
