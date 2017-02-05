import logging

import cscore as cs
import cv2
import numpy as np

import robotmap
from commands.rumblecontroller import RumbleController

logging.basicConfig(level=logging.INFO)


class Camera:
    """
    This subsystem controls a USB camera and performs image processing.
    """

    def __init__(self, port, width, height, fps, httpport):
        '''Instantiates objects.'''

        self.logger = logging.getLogger("robot")

        camera = cs.UsbCamera("usbcam", port)
        camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, width, height, fps)

        self.cv_sink = cs.CvSink("cvsink")
        self.cv_sink.setSource(camera)
        self.cv_source = cs.CvSource("cvsource", width, height, fps)

        # set up image server
        mjpeg_server = cs.MjpegServer("httpserver", httpport)
        mjpeg_server.setSource(self.cv_source)
        self.logger.info("mjpg server listening at http://0.0.0.0:{}".format(httpport))

        self.frame = np.zeros(shape=(width, height, 3), dtype=np.uint8)

        self.tape_contours = None  # tuple of pixel coords of tape contours
        self.rod_pos = None  # tuple of coords of rod as fraction of full width and height

        # hsv range for tape contour detection
        self.min_h, self.min_s, self.min_v = 45, 140, 100
        self.max_h, self.max_s, self.max_v = 65, 210, 130


    def update_frame(self):
        time, self.frame = self.cv_sink.grabFrame(self.frame)
        if time == 0:
            self.logger.error("error:", self.cv_sink.getError())

    def serve_frame(self):
        self.cv_source.putFrame(self.frame)

    def update_rod_pos(self):
        """
        Updates (x, y) coords of rod as fractions of width and height of frame, respectively.
        """
        if self.tape_contours is None:  # no tape contours
            self.logger.critical("Couldn't find the rod!")
            RumbleController(1).start()
            self.rod_pos = None
            return

        moments1 = cv2.moments(self.tape_contours[0])
        center1 = (moments1['m10'] / moments1['m00'], moments1['m01'] / moments1['m00'])  # center of one tape strip
        moments2 = cv2.moments(self.tape_contours[1])
        center2 = (moments2['m10'] / moments2['m00'], moments2['m01'] / moments2['m00'])  # center of other tape strip

        self.rod_pos = ((center1[0] + center2[0]) / 2 / robotmap.cameras.front_camera_width, (
            center1[1] + center2[1]) / 2 / robotmap.cameras.front_camera_height)

    def get_rod_pos(self):
        return self.rod_pos

    def draw_crosshairs(self):
        """
        Draws red crosshairs on frame.
        """
        center_x = self.frame.shape[0] // 2
        center_y = self.frame.shape[1] // 2
        # horizontal line
        self.frame[center_y][center_x - 10:center_x + 11][0] = 0
        self.frame[center_y][center_x - 10:center_x + 11][1] = 0
        self.frame[center_y][center_x - 10:center_x + 11][2] = 255
        # vertical line
        self.frame[center_y - 10:center_y + 11][center_x][0] = 0
        self.frame[center_y - 10:center_y + 11][center_x][1] = 0
        self.frame[center_y - 10:center_y + 11][center_x][2] = 255

    def draw_tape_contours(self):
        """
        Draws tape contours in green on frame.
        """
        if self.tape_contours is not None:
            cv2.drawContours(self.frame, self.tape_contours, -1, (100, 255, 100), 2)

    def update_tape_contours(self):
        """
        Finds two largest green four-sided contours.
        """
        # filter green
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([self.min_h, self.min_s, self.min_v]), np.array([self.max_h, self.max_s, self.max_v]))

        # find two most likely retro-reflective tape contours
        contours = cv2.findContours(mask, cv2.cv.CV_RETR_TREE, cv2.cv.CV_CHAIN_APPROX_SIMPLE)[0]
        # two largest four-sided contours
        largest = (0, 0)  # (contour, area)
        second_largest = (0, 0)
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

        if second_largest[0] == 0:  # if did not find two tape strips
            self.tape_contours = None
        else:
            self.tape_contours = (largest[0], second_largest[0])
