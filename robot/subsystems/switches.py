from wpilib.command.subsystem import Subsystem


# FIXME: Switches should be an input, not a subsystem. As we are not using them, I have not converted this over.
class Switches(Subsystem):
    def __init__(self):
        """
        Instantiates the switch objects.
        """

        super().__init__('Switch')

        # self.limit_switch = wpilib.DigitalInput(robotmap.switches.limit_switch_channel)
