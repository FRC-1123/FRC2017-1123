class PropertiesList:
    """
    Dummy class used to store variables on an object.
    """
    pass


motors = PropertiesList()
motors.left_id = 1
motors.right_id = 0

joystick = PropertiesList()
joystick.port = 0
joystick.top_left_port = 3
joystick.top_right_port = 4

# for xbox
joystick.left_port = 1
joystick.right_port = 5

cameras = PropertiesList()
cameras.front_camera_port = 0
cameras.front_camera_width = 320
cameras.front_camera_height = 240
cameras.front_camera_fps = 30

gear_mech = PropertiesList()
gear_mech.forward_solenoid_channel = 1
gear_mech.reverse_solenoid_channel = 0

switches = PropertiesList()
switches.limit_switch_channel = 0
