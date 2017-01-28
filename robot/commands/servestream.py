import logging

from wpilib.command import Command

import subsystems

logging.basicConfig(level=logging.DEBUG)


class ServeStream(Command):
    '''
    This command will serve the camera stream.
    '''

    def __init__(self):
        super().__init__("Serve Camera Stream")

        self.requires(subsystems.front_camera)

    def execute(self):
        subsystems.front_camera.update_frame()

        # draw shapes
        if subsystems.front_camera.tape_contours is not None:
            subsystems.front_camera.draw_tape_contours()
        subsystems.front_camera.draw_crosshairs()

        subsystems.front_camera.serve_frame()
