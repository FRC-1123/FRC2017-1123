import cscore as cs
import numpy as np
import cv2
import robotmap
from wpilib.command.subsystem import Subsystem


class Camera(Subsystem):
    '''
    This subsystem controls the USB camera.
    '''

    def __init__(self):
        '''Instantiates objects.'''
        # TODO: combine into one server

        super().__init__('Camera')

        camera = cs.UsbCamera("usbcam", 0)
        camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, robotmap.cameras.front_camera_width,
                            robotmap.cameras.front_camera_height,
                            robotmap.cameras.front_camera_fps)  # width, height, fps

        self.cv_sink = cs.CvSink("cvsink")
        self.cv_sink.setSource(camera)
        self.cv_source = cv.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG,

        # set up image server
        mjpeg_server = cs.MjpegServer("httpserver", 8081)
        mjpeg_server.setSource(self.cv_source)
                                            robotmap.cameras.front_camera_width, robotmap.cameras.front_camera_height,
                                            robotmaps.cameras.front_camera_fps)
        print("mjpg server listening at http://0.0.0.0:8081")

        self.frame = np.zeros(
            shape=(robotmap.cameras.front_camera_width, robotmap.cameras.front_camera_height, 3), dtype=np.uint8)
            shape=(robotmap.cameras.front_camera_width, robotmap.cameras.front_camera_height, 3), dtype=np.uint8)

        self.tape_contours = None

    def draw_crosshairs(self):
        '''
        Draws red crosshairs.
        '''
        center_x = self.frame.shape[0] // 2
        center_y = self.frame.shape[1] // 2
        # horizontal line
        self.frame[center_y][center_x-10:center_x+11][0] = 0
        self.frame[center_y][center_x-10:center_x+11][1] = 0
        self.frame[center_y][center_x-10:center_x+11][2] = 255
        # vertical line
        self.frame[center_y-10:center_y+11][center_x][0] = 0
        self.frame[center_y-10:center_y+11][center_x][1] = 0
        self.frame[center_y-10:center_y+11][center_x][2] = 255


    def draw_tape_contours(self):
        '''
        Draws the tape contours in green.
        '''
        cv2.drawContours(self.frame, self.tape_contours, -1, (100, 255, 100), 2)

    def find_tape_contours(self):
        '''
        Finds the two largest green four-sided contours.
        '''
        # filter green
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([45, 140, 100]), np.array([65, 210, 130]))
        
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
            approx = cv2.approxPolyDP(c, .05*perim, True)
            if len(approx) != 4:  # only consider quadrilaterals
                continue
            if area > largest[1]:
                second_largest = largest
                largest = (c, area)
            elif area > second_largest[1]:
                second_largest = (c, area)

        if second_largest[0] == 0:  # if did not find two tape strips
            self.tape_contours = None
        self.tape_contours = (largest[0], second_largest[0])

    def initDefaultCommand(self):
        self.setDefaultCommand(ServeCrosshairStream())
