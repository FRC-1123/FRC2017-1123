# Import the camera server
from cscore import CameraServer
import robotmap
import logging

# Import OpenCV and NumPy
import cv2
import numpy as np


class Camera:
    def main(self):
        cs = CameraServer.getInstance()
        cs.enableLogging()

        # Capture from the first USB Camera on the system
        camera = cs.startAutomaticCapture()
        camera.setResolution(robotmap.cameras.camera_width, robotmap.cameras.camera_height)

        # Get a CvSink. This will capture images from the camera
        cv_sink = cs.getVideo()

        # (optional) Setup a CvSource. This will send images back to the Dashboard
        output_stream = cs.putVideo("Camera Feed", robotmap.cameras.camera_width, robotmap.cameras.camera_height)

        # Allocating new images is very expensive, always try to preallocate
        self.frame = np.zeros(shape=(robotmap.cameras.camera_height, robotmap.cameras.camera_width, 3), dtype=np.uint8)

        self.tape_contours = None  # tuple of pixel coords of tape contours
        self.rod_pos = None  # tuple of coords of rod as fraction of full width and height
        self.no_rod_count = 0  # how many loops without being able to find the rod
        self.no_rod_count_max = 5  # how many loops of not being able to find the rod before setting rod_pos = None

        # hsv range for tape contour detection
        self.min_h, self.min_s, self.min_v = 65, 100, 100
        self.max_h, self.max_s, self.max_v = 115, 255, 255

        self.logger = logging.getLogger("robot")

        while True:
            # Tell the CvSink to grab a frame from the camera and put it
            # in the source image.  If there is an error notify the output.
            time, self.frame = cv_sink.grabFrame(self.frame)
            if time == 0:
                # Send the output the error.
                output_stream.notifyError(cv_sink.getError())
                # skip the rest of the current iteration
                continue

            self.update_tape_contours()
            self.update_rod_pos()

            # draw shapes
            self.draw_crosshairs()
            self.draw_tape_contours()
            self.draw_rod_pos()

            # (optional) send some image back to the dashboard
            output_stream.putFrame(self.frame)


    def update_rod_pos(self):
        """
        Updates (x, y) pixel coords of rod.
        """
        if self.tape_contours is None:  # no tape contours
            self.no_rod_count += 1
            if self.no_rod_count >= self.no_rod_count_max:
                self.rod_pos = None
        else:
            self.no_rod_count = 0
            moments1 = cv2.moments(self.tape_contours[0])
            center1 = (moments1['m10'] / moments1['m00'], moments1['m01'] / moments1['m00'])  # center of one tape strip
            moments2 = cv2.moments(self.tape_contours[1])
            center2 = (moments2['m10'] / moments2['m00'], moments2['m01'] / moments2['m00'])  # center of other tape strip

            self.rod_pos = (int((center1[0] + center2[0]) / 2), int((center1[1] + center2[1]) / 2))

    def get_rod_pos(self):
        """
        Returns (x, y) coords of rod as fractions of the frame's width and height, respectively.
        """
        if self.rod_pos is None:
            return None
        return self.rod_pos[0] / robotmap.cameras.front_camera_width, self.rod_pos[1] / robotmap.cameras.front_camera_height

    def draw_rod_pos(self):
        """
        Draws a red point of radius 5 pixels on the frame at the rod's position.
        """
        if self.rod_pos is not None:
            cv2.circle(self.frame, self.rod_pos, 5, (0, 0, 255), -1)

    def draw_crosshairs(self):
        """
        Draws red crosshairs on frame.
        """
        center_x = self.frame.shape[1] // 2
        center_y = self.frame.shape[0] // 2
        # horizontal line
        self.frame[center_y, center_x - 10:center_x + 11] = [0, 0, 255]
        # vertical line
        self.frame[center_y - 10:center_y + 11, center_x] = [0, 0, 255]

    def draw_tape_contours(self):
        """
        Draws tape contours in green on frame.
        """
        if self.tape_contours is not None:
            cv2.drawContours(self.frame, self.tape_contours, -1, (0, 255, 0), 2)

    def update_tape_contours(self):
        """
        Finds two largest green four-sided contours.
        """
        # filter green
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([self.min_h, self.min_s, self.min_v]), np.array([self.max_h, self.max_s, self.max_v]))

        # find two most likely retro-reflective tape contours
        contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        # two largest four-sided contours
        largest = (None, 0)  # (contour, area)
        second_largest = (None, 0)
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

        if second_largest[0] is None:  # if did not find two tape strips
            self.tape_contours = None
        else:
            self.tape_contours = (largest[0], second_largest[0])


def start():
    front_camera = Camera()
    front_camera.main()
