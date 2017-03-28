import logging

from networktables import NetworkTables
from wpilib import GenericHID
from wpilib.command import Command
from wpilib.timer import Timer

from commands.controlgearmech import ControlGearMech
from commands.followjoystick import FollowJoystick
from commands.lockon import LockOn
from commands.rumblecontroller import RumbleController
from commands.switchcamera import SwitchCamera
from inputs import oi

logging.basicConfig(level=logging.INFO)


class RespondToController(Command):
    """
    This command will respond to the controller's buttons.
    """

    def __init__(self):
        super().__init__("Respond to Controller")

        self.sd = NetworkTables.getTable("SmartDashboard")
        self.logger = logging.getLogger("robot")

        oi.start_btn.whenPressed(SwitchCamera())

        self.timer = Timer()
        self.timer.start()

        self.right_bumper_last = False
        self.left_bumper_last = False

    def execute(self):
        if self.timer.hasPeriodPassed(0.05):
            # for xbox controller

            # piston control
            if oi.controller.getAButton():  # open
                ControlGearMech(False).start()
            elif oi.controller.getBButton():  # close
                ControlGearMech(True).start()

                # reversing control
                # if oi.controller.getStartButton():  # reverse camera, motors, and sonar
                # if self.sd.containsKey("camera/dev"):
                #     if self.sd.getNumber("camera/dev") == 1:
                #         self.sd.putNumber("camera/dev", 2)
                #     else:
                #         self.sd.putNumber("camera/dev", 1)
                # else:
                #     self.sd.putNumber("camera/dev", 1)
                # cur_direct = self.sd.getNumber("direction")
                # if cur_direct == 1:
                #     subsystems.motors.reverseDirection()
                # else:
                #     subsystems.motors.forwardDirection()
                # self.sd.putNumber("direction", -cur_direct)

            # slow mode
            if oi.controller.getBumper(GenericHID.Hand.kRight):
                if self.right_bumper_last:
                    pass
                elif oi.divider != 1:
                    self.sd.putBoolean("slowmode", False)
                else:
                    self.sd.putBoolean("slowmode", True)
                self.right_bumper_last = True
            else:
                self.right_bumper_last = False

            # lock on
            if oi.controller.getBumper(GenericHID.Hand.kLeft):
                if self.left_bumper_last:
                    pass
                elif not self.sd.getBoolean("lockonRunning"):
                    LockOn().start()
                else:
                    self.logger.critical("Returning control to the controller!")
                    self.sd.putBoolean("lockonRunning", False)
                    RumbleController(0.5).start()
                    FollowJoystick().start()
                self.left_bumper_last = True
            else:
                self.left_bumper_last = False

                # rod_pos = camera.get_rod_pos()
                # if rod_pos is None:  # cannot find rod
                #     self.logger.critical("Couldn't find the rod! {}".format(rod_pos))
                #     RumbleController(0.5).start()
                # else:
                #     self.logger.info("Driving to the rod!")
                #     DriveToRod().start()

                # for single joystick
                # if oi.joystick.getRawButton(robotmap.joystick.top_left_port):  # piston in
                #     subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kReverse)
                #     self.sd.putBoolean("pneumatic", False)
                # elif oi.joystick.getRawButton(robotmap.joystick.top_right_port):  # piston out
                #     subsystems.gear_mech.double_solenoid.set(subsystems.gear_mech.double_solenoid.Value.kForward)
                #     self.sd.putBoolean("pneumatic", True)
