from wpilib import Timer
from wpilib.command import Command

from inputs import cameras


class ServeStream(Command):
    """
    This command serves the camera stream.
    """

    def __init__(self):
        super().__init__("Serve Camera Stream")

        self.timer = Timer()
        self.timer.start()

    def execute(self):
        cameras.front_camera.update_frame()
        cameras.front_camera.update_tape_contours()
        cameras.front_camera.update_rod_pos()

        # draw shapes
        cameras.front_camera.draw_crosshairs()
        cameras.front_camera.draw_tape_contours()
        cameras.front_camera.draw_rod_pos()

        cameras.front_camera.serve_frame()
