import logging

import subsystems
from wpilib.command import Command

logging.basicConfig(level=logging.DEBUG)


class ServeCrosshairStream(Command):
    '''
    This command will serve the camera stream.
    '''

    def __init__(self):
        super().__init__("Serve Camera Stream")

        self.requires(subsystems.front_camera)

    def execute(self):
        time, frame = subsystems.front_camera.cv_sink.grabFrame(subsystems.front_camera.frame)
        if time == 0:
            print("error:", subsystems.front_camera.cv_sink.getError())
            return

        print("got frame at time", time, frame.shape)

        # draw crosshair
        center_x = frame.shape[0] // 2
        center_y = frame.shape[1] // 2
        # horizontal line
        frame[center_y][center_x - 10:center_x + 11][0] = 0
        frame[center_y][center_x - 10:center_x + 11][1] = 0
        frame[center_y][center_x - 10:center_x + 11][2] = 255
        # vertical line
        frame[center_y - 10:center_y + 11][center_x][0] = 0
        frame[center_y - 10:center_y + 11][center_x][1] = 0
        frame[center_y - 10:center_y + 11][center_x][2] = 255

        subsystems.front_camera.cv_source.putFrame(frame)
