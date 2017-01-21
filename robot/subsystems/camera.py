import wpilib
from wpilib.command.subsystem import Subsystem

import robotmap

import cscore as cs
import numpy as np
import cv2


class Camera(Subsystem):
    '''
    This subsystem controls the USB camera.
    '''

    def __init__(self):
        '''Instantiates objects.'''
        # TODO: combine into one server
        
        super().__init__('Camera')
        
        camera = cs.UsbCamera("usbcam", 0)
        camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, robotmap.cameras.front_camera_width, robotmap.cameras.front_camera_height, robotmap.cameras.front_camera_fps)  # width, height, fps
        
        self.cv_sink = cs.CvSink("cvsink")
        self.cv_sink.setSource(camera)

        # serves images with a crosshair at the center
        self.crosshair_mjpeg_server = cs.MjpegServer("crosshair_httpserver", 8081)
        self.crosshair_mjpeg_server.setSource(camera)
        self.crosshair_source = cv.CvSource("crosshair_source", cs.VideoMode.PixelFormat.kMJPEG, robotmap.cameras.front_camera_width, robotmap.cameras.front_camera_height, robotmaps.cameras.front_camera_fps)
        print("crosshair mjpg server listening at http://0.0.0.0:8081")

                
        # images for processing
        self.processing_mjpeg_server = cs.MjpegServer("processing_httpserver", 8082)
        self.processing_mjpeg_server.setSource(cv_source)
        self.processing_source = cv.CvSource("processing_source", cs.VideoMode.PixelFormat.kMJPEG, robotmap.cameras.front_camera_width, robotmap.cameras.front_camera_height, robotmap.cameras.front_camera_fps)
        print("OpenCV output mjpg server listening at http://0.0.0.0:8082")

        self.crosshair_frame = np.zeros(shape=(robotmap.cameras.front_camera_width, robotmap.cameras.front_camera_height, 3), dtype=np.uint8)
        self.processing_frame = np.zeros(shape=(robotmap.cameras.front_camera_width, robotmap.cameras.front_camera_height, 3), dtype=np.uint8)
    
    def get_rod_position(self):
        pass

    def initDefaultCommand(self):
        self.setDefaultCommand(ServeCrosshairStream())
