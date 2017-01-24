import logging

import cv2
import robotmap
import subsystems
import wpilib
from wpilib.command import Command

logging.basicConfig(level=logging.INFO)


class DriveToRod(Command):
    '''
    This command will find the rod and drive the robot towards it.
    '''

    def __init__(self):
        super().__init__("Drive To Rod")

        # PID constants
        self.kp = 15
        self.ki = 0
        self.kd = 0

        # used for calculating PID derivative and integral
        self.timer = wpilib.Timer()
        self.timer.start()
        self.prev_error = 0
        self.prev_time = self.timer.get()

        self.requires(subsystems.front_camera)
        self.requires(subsystems.motors)

    def execute(self):
        center = self.get_center()
        if not self.get_center:
            print("Couldn't find the rod!")
            return
        center_x = center[0] / robotmap.cameras.front_camera_width
        error = .5 - center_x
        print("current rod error:", error)
        if abs(error) > .02:  # only use PID if error greater than 2%
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

    def get_rod_pos(self):
        time, frame = subsystems.front_camera.cv_sink.grabFrame(subsystems.front_camera.frame)
        if time == 0:
            print("error:", subsystems.front_camera.cv_sink.getError())
            return False

        tape1, tape2 = subsystems.tape_contours
        
        # find position of rod
        moments1 = cv2.moments(tape1)
        center1 = (moments1['m10'] // moments1['m00'], moments1['m01'] // moments1['m00'])  # center of first tape strip
        moments2 = cv2.moments(tape2)
        center2 = (
            moments2['m10'] // moments2['m00'], moments2['m01'] // moments2['m00'])  # center of second tape strip

        return (center1[0] + center2[0]) // 2, (center1[1] + center2[1]) // 2
