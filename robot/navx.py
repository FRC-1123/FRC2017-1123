from robotpy_ext.common_drivers.navx import AHRS

ahrs = None


def init():
    """
    Initialize NavX object.
    """
    ahrs = AHRS.create_spi()
    ahrs.reset()
