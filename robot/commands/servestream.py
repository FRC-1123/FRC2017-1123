import logging

from wpilib.command import Command

import cameras

logging.basicConfig(level=logging.DEBUG)


class ServeStream(Command):
    """
    This command serves the camera stream.
    """

    def __init__(self):
        super().__init__("Serve Camera Stream")

    def execute(self):
        cameras.front_camera.update_frame()

        # draw shapes
        if cameras.front_camera.tape_contours is not None:
            cameras.front_camera.draw_tape_contours()
        cameras.front_camera.draw_crosshairs()

        cameras.front_camera.serve_frame()
