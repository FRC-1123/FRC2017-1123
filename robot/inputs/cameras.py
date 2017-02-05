import robotmap
from camera import Camera

front_camera = None


def init():
    global front_camera

    front_camera = Camera(robotmap.cameras.front_camera_port, robotmap.cameras.front_camera_width, robotmap.cameras.front_camera_height,
                          robotmap.cameras.front_camera_fps, robotmap.cameras.front_camera_httpport)
