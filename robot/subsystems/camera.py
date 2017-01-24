import cscore as cs
import numpy as np
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

    def draw_crosshairs(self):
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


    def initDefaultCommand(self):
        self.setDefaultCommand(ServeCrosshairStream())
