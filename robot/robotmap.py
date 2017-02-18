class PropertiesList:
    """
    Dummy class used to store variables on an object.
    """
    pass


motors = PropertiesList()
motors.left_id = 1
motors.right_id = 0
motors.left_follower_id = 3
motors.right_follower_id = 2

joystick = PropertiesList()
joystick.port = 0
joystick.forwardAxis = 5
joystick.steeringAxis = 4

cameras = PropertiesList()
cameras.camera_width = 320
cameras.camera_height = 240

gear_mech = PropertiesList()
gear_mech.forward_solenoid_channel = 1
gear_mech.reverse_solenoid_channel = 0

sonar = PropertiesList()
sonar.front_channel = 0
sonar.back_channel = 4

# switches = PropertiesList()
# switches.limit_switch_channel = 0
