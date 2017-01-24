import logging

import subsystems
from wpilib.command import Command

logging.basicConfig(level=logging.DEBUG)


class ServeStream(Command):
    '''
    This command will serve the camera stream.
    '''

    def __init__(self):
        super().__init__("Serve Camera Stream")

        self.requires(subsystems.front_camera)

    def execute(self):
        # grab frame
        time, subsystems.front_camera.frame = subsystems.front_camera.cv_sink.grabFrame(subsystems.front_camera.frame)
        if time == 0:
            print("error:", subsystems.front_camera.cv_sink.getError())
            return
        print("got frame at time", time, frame.shape)

        # draw shapes
        if subsystems.front_camera.tape_contours is not None:
            subsystems.front_camera.draw_tape_contours()
        subsystems.front_camera.draw_crosshairs()

        # serve frame
        subsystems.front_camera.cv_source.putFrame(frame)
