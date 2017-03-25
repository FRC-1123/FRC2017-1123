import logging

from wpilib.command.commandgroup import CommandGroup

# from commands.driveforward import DriveForward
from commands.setspeed import SetSpeed
from commands.drivetorod import DriveToRod
from commands.rotate import Rotate


class AutonomousProgram(CommandGroup):
    def __init__(self, mode):
        super().__init__('Autonomous Program')
        self.logger = logging.getLogger("robot")

        if mode == "left":
            # self.addSequential(SetSpeed(-0.3, 0.5))
            # self.addSequential(Rotate(-20))
            # self.addSequential(SetSpeed(-0.3, 2.5))
            # self.addSequential(Rotate(28))
            # self.addSequential(DriveToRod(timeout=3.5))

            # self.addSequential(DriveForward(24))
            self.addSequential(SetSpeed(0.2, 0.5))
            self.addSequential(Rotate(-20))
            # self.addSequential(DriveForward(48))
            self.addSequential(SetSpeed(0.2, 1.5))
            self.addSequential(Rotate(30))
            self.addSequential(DriveToRod(timeout=3.5))
            # if switches.gear_mech_switch.get():
            #     self.addSequential(ControlGearMech(False))
            #     self.addSequential(DriveBackward(3))


            # self.addSequential(ControlGearMech(False))
            # self.addSequential(WaitCommand())
            # self.addSequential(SetSpeed(0.3, 0.1))
            # self.addSequential(WaitCommand(1))
            # self.addSequential(SetSpeed(0.3, 1))
            # self.addParallel(ControlGearMech(True))
            # self.addSequential(Rotate(-10))
            # self.addSequential(SetSpeed(-0.5, 2))
        elif mode == "right":
            # self.addSequential(SetSpeed(-0.3, 0.5))
            # self.addSequential(Rotate(20))
            # self.addSequential(SetSpeed(-0.3, 2.5))
            # self.addSequential(Rotate(-28))
            # self.addSequential(DriveToRod(timeout=3.5))

            # self.addSequential(DriveForward(24))
            self.addSequential(SetSpeed(0.2, 0.5))
            self.addSequential(Rotate(20))
            # self.addSequential(DriveForward(48))
            self.addSequential(SetSpeed(0.2, 1.5))
            self.addSequential(Rotate(-30))
            self.addSequential(DriveToRod(timeout=3.5))
            # if switches.gear_mech_switch.get():
            #     self.addSequential(ControlGearMech(False))
            #     self.addSequential(DriveBackward(3))

            # self.addSequential(ControlGearMech(False))
            # self.addSequential(WaitCommand(0.5))
            # self.addSequential(SetSpeed(0.3, 0.1))
            # self.addSequential(WaitCommand(1))
            # self.addSequential(SetSpeed(0.3, 1))
            # self.addParallel(ControlGearMech(True))
            # self.addSequential(Rotate(10))
            # self.addSequential(SetSpeed(-0.5, 2))
        else:
            # self.addSequential(DriveForward(36))
            self.addSequential(SetSpeed(0.2, 1.0))
            self.logger.info("Drive to rod now!")
            self.addSequential(DriveToRod(timeout=3.5))
            # if switches.gear_mech_switch.get():
            #     self.addSequential(ControlGearMech(False))
            #     self.addSequential(DriveBackward(3))
            # self.addSequential(ControlGearMech(False))
            # self.addSequential(WaitCommand(0.5))
            # self.addSequential(SetSpeed(0.3, 0.1))
            # self.addSequential(WaitCommand(1))
            # self.addSequential(SetSpeed(0.3, 1))
            # self.addParallel(ControlGearMech(True))
            # self.addSequential(Rotate(60))
            # self.addSequential(SetSpeed(-0.5, 1))
            # self.addSequential(Rotate(-60))
            # self.addSequential(SetSpeed(-0.5, 2))
