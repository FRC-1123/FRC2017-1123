from robotpy_ext.common_drivers.navx import AHRS

ahrs = None


def init():
    """
    Initialize NavX object.
    """
    global ahrs

    ahrs = AHRS.create_spi()
