class GearedMotor:
    """
    Container class for motors used with JohnnyV.
    Motors: GHM02
    """

    def __init__(self, pin, init_percentage, init_direction, pulse_width):
        """
        :param pin: Corresponding servo pin on the SSC32U board, i.e 13.
        :param init_percentage: Initial speed of geared motor, i.e 10(%).
        :param init_direction: Initial direction of geared motor, i.e 1 (forward).
        :param pulse_width: Pulse width in milliseconds, i.e 1000.

        """
        self.pin = pin
        self.init_percentage = init_percentage
        self.init_direction = init_direction
        self.pulse_width = pulse_width
