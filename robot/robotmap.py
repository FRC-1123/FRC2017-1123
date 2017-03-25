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
joystick.forwardAxis = 1
joystick.steeringAxis = 4

cameras = PropertiesList()
cameras.camera_width = 320
cameras.camera_height = 240
cameras.dev1 = 1
cameras.dev2 = 0

gear_mech = PropertiesList()
gear_mech.forward_solenoid_channel = 1
gear_mech.reverse_solenoid_channel = 0

climbing_mech = PropertiesList()
climbing_mech.id = 4
climbing_mech.follower_id = 5

sonar = PropertiesList()
sonar.front_channel = 6
sonar.front_right_channel = 4
sonar.right_channel = 2
sonar.back_right_channel = 3
sonar.back_channel = 1
sonar.back_left_channel = 5
sonar.left_channel = 0
sonar.front_left_channel = 7
sonar.pinger_channel = 8

switches = PropertiesList()
switches.gear_switch_channel = 9
