'''
By storing port numbers here, we can easily change the "wiring" of the robot
from a single location. Instantiate a PortsList for each subsystem and assign
port numbers as needed.
'''


class PropertiesList:
    '''Dummy class used to store variables on an object.'''
    pass


motors = PropertiesList()
motors.left_id = 0
motors.right_id = 1

joystick = PropertiesList()
joystick.port = 0
joystick.left_port = 5
joystick.right_port = 1

cameras = PropertiesList()
cameras.front_camera_port = 0
cameras.front_camera_width = 320
cameras.front_camera_height = 240
cameras.front_camera_fps = 30
