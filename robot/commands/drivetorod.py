import wpilib
from wpilib.command import Command
import subsystems
import robotmap

import cv2

import logging

logging.basicConfig(level=logging.DEBUG)


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
        center_x = self.get_center()[0] / robotmap.cameras.front_camera_width
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

    def get_center(self):
        time, frame = subsystems.front_camera.cv_sink.grabFrame(subsystems.front_camera.processing_frame)
        if time == 0:
            print("error:", subsystems.front_camera.cv_sink.getError())
            return

        # filter only green
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([45, 140, 100]), np.array([65, 210, 130]))

        # find relevant retro-reflective tape contours
        contours = cv2.findContours(mask, cv2.cv.CV_RETR_TREE, cv2.cv.CV_CHAIN_APPROX_SIMLE)[0]
        # find two largest four-sided contours
        largest = (0, 0)  # (contour, area)
        second_largest = (0, 0)  # (contour, area)
        for c in contours:
            area = cv2.contourArea(c)
            if area < 100:  # remove noise
                continue
            perim = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, .05 * perim, True)
            if len(approx) != 4:  # only consider quadrilaterals
                continue
            if area > largest[1]:
                second_largest = largest
                largest = (c, area)
            elif area > second_largest[1]:
                second_largest = (c, area)

        if second_largest[0] == 0:  # if did not find the tape strips
            return False

        # find position of rod
        moments1 = cv2.moments(largest[0])
        center1 = (moments1['m10'] // moments1['m00'], moments1['m01'] // moments1['m00'])  # center of first tape strip
        moments2 = cv2.moments(second_largest[0])
        center2 = (
        moments2['m10'] // moments2['m00'], moments2['m01'] // moments2['m00'])  # center of second tape strip

        return (center1[0] + center2[0]) // 2, (center1[1] + center2[1]) // 2
