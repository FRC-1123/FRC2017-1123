'''
By storing port numbers here, we can easily change the "wiring" of the robot
from a single location. Instantiate a PortsList for each subsystem and assign
port numbers as needed.
'''

class PortsList:
    '''Dummy class used to store variables on an object.'''
    pass


motors = PortsList()
motors.left_id = 0
motors.right_id = 1

joystick = PortsList()
joystick.port = 0
joystick.left_port = 5
joystick.right_port = 1