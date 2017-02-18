"""
These are a set of drivers for the XL-MaxSonar EZ series of sonar modules.
The devices have a few different ways of reading from them, and the these drivers attempt to cover
some of the methods
"""

from robotpy_ext.common_drivers.xl_max_sonar_ez import MaxSonarEZPulseWidth
from robotpy_ext.common_drivers.xl_max_sonar_ez import units


class HRLVMaxSonarEZPulseWidth(MaxSonarEZPulseWidth):
    """
    This is a driver for the MaxSonar EZ series of sonar sensors, using the pulse-width output of the sensor.

    To use this driver, pin 2 on the sensor must be mapped to a dio pin.
    """

    verified = True

    def __init__(self, channel, output_units=units.inch):
        """Sonar sensor constructor

        :param channel: The digital input index which is wired to the pulse-width output pin (pin 2) on the sensor.
        :param output_units: The Unit instance specifying the format of value to return
        """

        # Call the parents
        super().__init__(channel, output_units)

    def get(self):
        """Return the current sonar sensor reading, in the units specified from the constructor"""
        centimeters = self.counter.getPeriod() / 0.000010
        return units.convert(units.centimeter, self.output_units, centimeters)
