'''
All subsystems should be imported here and instantiated inside the init method.
If you want your subsystem to be accessible to commands, you must add a variable
for it in the global scope.
'''

from wpilib.robotbase import RobotBase

from .gearmech import GearMech
from .motors import Motors

motors = None
gear_mech = None


# front_camera = None


def init():
    '''
    Creates all subsystems. You must run this before any commands are
    instantiated. Do not run it more than once.
    '''
    global motors, gear_mech

    '''
    Some tests call startCompetition multiple times, so don't throw an error if
    called more than once in that case.
    '''
    if motors is not None and not RobotBase.isSimulation():
        raise RuntimeError('Subsystems have already been initialized')

    motors = Motors()

    #    front_camera = Camera()

    gear_mech = GearMech() 
