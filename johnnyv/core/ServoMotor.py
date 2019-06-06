from johnnyv.core.Observer import Observer


class ServoMotor(Observer):
    """
    Container class for servos used with JohnnyV.
    Servos: HS475, HS485HB, HS645MG, HS422
    """
    def __init__(self, dependencies, pin, max_pulse, min_pulse, abs_max_pulse, abs_min_pulse, pulse_width, init_pulse):
        """
        :param dependencies: Inter-Servo dependencies.
        :param pin: Corresponding servo pin on the SSC32U board, i.e 13.
        :param max_pulse: Maximum allowed servo pulse, i.e 2400 (Software-depended).
        :param min_pulse: Minimum allowed servo pulse, i.e 600 (Software-depended).
        :param abs_max_pulse: Absolute maximum pulse allowed, i.e 2500 (Hardware-depended).
        :param abs_min_pulse: Absolute minimum pulse allowed, i.e 500  (Hardware-depended).
        :param pulse_width: Pulse width in milliseconds, i.e 1000.
        :param init_pulse: Initial position of servo, i.e 1500.

        """
        self.dependencies = dependencies
        self.pin = pin
        self.max_pulse = max_pulse
        self.min_pulse = min_pulse
        self.pulse_span = abs(max_pulse-min_pulse)
        self.abs_max_pulse = abs_max_pulse
        self.abs_min_pulse = abs_min_pulse
        self.pulse_width = pulse_width
        self.init_pulse = init_pulse
        self.current_position = init_pulse

    def update(self, pin, degree):
        """
        :param pin: Corresponding servo pin on the SSC32U board.
        :param degree: Servo pulse in degrees, i.e 90.
        :return: False.

        Method to notify specific servomotor about changes.
        """
        if pin in self.dependencies:
            return False
        # TODO: implement method and add return value. Add the corresponding return value to the docstring :return:.









