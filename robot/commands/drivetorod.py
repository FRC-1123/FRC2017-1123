import logging

import wpilib
from wpilib.command import Command

import subsystems

logging.basicConfig(level=logging.INFO)


class DriveToRod(Command):
    '''
    This command will find the rod and drive the robot towards it.
    '''

    def __init__(self):
        super().__init__("Drive To Rod")

        # PID constants
        self.kp = 0.06
        self.ki = 0
        self.kd = 0
        self.ktolerance = 0.02

        # used for calculating PID derivative and integral
        self.timer = wpilib.Timer()
        self.timer.start()
        self.prev_error = 0
        self.prev_time = self.timer.get()

        self.requires(subsystems.motors)

    def execute(self):
        rod_pos = subsystems.front_camera.get_rod_pos()
        if rod_pos is None:
            print("Couldn't find the rod!")
            return
        error = .5 - rod_pos[0]  # error as horizontal distance from center
        print("current rod error:", error)
        if abs(error) > self.ktolerance:  # only use PID if error greater than tolerance
            curve = self.calc_pid(error)
        else:
            curve = 0
        subsystems.motors.robot_drive.drive(.5, curve)

    def calc_pid(self, error):
        time = self.timer.get()
        e_deriv = (error - self.prev_error) / (time - self.prev_time)
        e_int = (error + self.prev_error) / 2 * (time - self.prev_time)
        self.prev_error = error
        self.prev_time = time
        return self.kp * error + self.kd * e_deriv + self.ki * e_int
