from wpilib.command.commandgroup import CommandGroup

from commands.drivetorod import DriveToRod
from commands.rotate import Rotate
from commands.setspeed import SetSpeed
from commands.updatenetworktables import UpdateNetworkTables


class AutonomousProgram(CommandGroup):
    def __init__(self, mode):
        super().__init__('Autonomous Program')

        self.addParallel(UpdateNetworkTables())
        if mode == "left":
            self.addSequential(SetSpeed(0.5, 1))
            self.addSequential(Rotate(30))
            self.addSequential(DriveToRod(5))
        elif mode == "right":
            self.addSequential(SetSpeed(0.5, 1))
            self.addSequential(Rotate(-30))
            self.addSequential(DriveToRod(5))
        else:
            self.addSequential(DriveToRod(10))
