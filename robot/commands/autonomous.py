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
            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(Rotate(-20))
            self.addSequential(SetSpeed(-0.3, 2.1))
            self.addSequential(Rotate(30))
            self.addSequential(DriveToRod(3))
            self.addSequential(SetSpeed(0.3, 1))
            self.addSequential(Rotate(-10))
            self.addSequential(SetSpeed(-0.5, 2))
        elif mode == "right":
            self.addSequential(SetSpeed(-0.3, 0.5))
            self.addSequential(Rotate(20))
            self.addSequential(SetSpeed(-0.3, 2.1))
            self.addSequential(Rotate(-30))
            self.addSequential(DriveToRod(3))
            self.addSequential(SetSpeed(0.3, 1))
            self.addSequential(Rotate(10))
            self.addSequential(SetSpeed(-0.5, 2))
        else:
            self.addSequential(DriveToRod(5))
