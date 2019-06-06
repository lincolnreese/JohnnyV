import json
import numbers

from johnnyv.core.ServoMotor import ServoMotor
from johnnyv.core.GearedMotor import GearedMotor
from johnnyv.core.Controller import Controller


class Component:
    """
    Container class for all robot components
    """

    constants = json.load(open('/home/pi/johnnyv/ext/Constants.json'))

    def __init__(self, component):
        """
        :param component: Name of component, i.e 'left_arm'.
        """
        self.component = str(component).lower()
        self.servos = []
        self.motors = []

        tmp_servo_list = Component.constants['components'][self.component]['servo_list']
        tmp_motor_list = Component.constants['components'][self.component]['motor_list']

        if tmp_servo_list:
            self.servos = [ServoMotor(value['dependencies'],
                                      value['pin'],
                                      value['max_pulse'],
                                      value['min_pulse'],
                                      value['abs_max_pulse'],
                                      value['abs_min_pulse'],
                                      value['pulse_width'],
                                      value['init_pulse'])
                           for (key, value) in tmp_servo_list.items()]

        if tmp_motor_list:
            self.motors = [GearedMotor(value['pin'],
                                       value['init_percentage'],
                                       value['init_direction'],
                                       value['pulse_width']) for (key, value) in tmp_motor_list.items()]

        Controller.add_servos(self.servos)

    def set_property(self, prop_list):
        """
        :param prop_list: List of properties to be set.
        :return: True for successful setting.
        Sets desired properties to a servomotor.
        """
        if prop_list:
            if isinstance(prop_list, list):
                if all(isinstance(command, tuple) for command in prop_list):
                    if all(len(command) == 3 for command in prop_list):
                        if all(isinstance(number, numbers.Number) for command in prop_list for number in command[::2]):
                            if all(isinstance(command[1], str) for command in prop_list):
                                if self.servos:
                                    for command in prop_list:
                                        pin = command[0]
                                        servo = next(servo for servo in self.servos if servo.pin == pin)

                                        if servo:
                                            servo_property = command[1]
                                            new_value = command[2]
                                            prop_list.remove(command)

                                            if servo_property == 'max_pulse':
                                                if new_value <= servo.abs_max_pulse:
                                                    servo.max_pulse = new_value
                                                else:
                                                    self.error("'max_pulse' is greater than 'abs_max_pulse'.")
                                                    return False

                                            elif servo_property == 'min_pulse':
                                                if new_value >= servo.abs_min_pulse:
                                                    servo.min_pulse = new_value
                                                else:
                                                    self.error("'min_pulse' is less than 'abs_min_pulse'.")
                                                    return False

                                            elif servo_property == 'init_pulse':
                                                if servo.abs_min_pulse <= new_value <= servo.abs_max_pulse:
                                                    servo.init_pulse = new_value
                                                else:
                                                    self.error("'init_pulse' is not in allowed range.")
                                                    return False

                                            elif servo_property == 'pulse_width':
                                                if new_value > 0:
                                                    servo.pulse_width = new_value
                                                else:
                                                    self.error("'pulse_width' must be greater than 0.")
                                                    return False

                                            else:
                                                self.error('Not settable Property given: ' + servo_property + '.')
                                                return False

                                if self.motors:
                                    for command in prop_list:
                                        pin = command[0]
                                        motor = next(motor for motor in self.motors if motor.pin == pin)

                                        if motor:
                                            servo_property = command[1]
                                            new_value = command[2]
                                            prop_list.remove(command)

                                            if servo_property == 'init_percentage':
                                                if 0 <= new_value <= 100:
                                                    motor.init_percentage = new_value
                                                else:
                                                    self.error("'percentage' must be between 0 and 100.")
                                                    return False

                                            elif servo_property == 'init_direction':
                                                if new_value in [-1, 0, 1]:
                                                    motor.init_direction = new_value
                                                else:
                                                    self.error("value of 'direction' must be -1, 0 or 1.")
                                                    return False

                                            elif servo_property == 'pulse_width':
                                                if new_value >= 0:
                                                    motor.pulse_width = new_value
                                                else:
                                                    self.error("'pulse_width' must be greater than 0.")
                                                    return False
                                            else:
                                                self.error('Not settable Property given: ' + servo_property + '.')
                                                return False

                                if self.servos or self.motors:
                                    return True
                                else:
                                    self.error('No servo or motor list available.')
                                    return False
                            else:
                                self.error('Unexpected tuple element. Second element must be a string.')
                                return False
                        else:
                            self.error('Unexpected tuple element. First & third Element must be a number')
                            return False
                    else:
                        self.error('Unexpected tuple size. Expected tuple of three')
                        return False
                else:
                    self.error('Unexpected list element. Expected list of tuples')
                    return False
            else:
                self.error('Unexpected input: ' + type(prop_list).__name__ + '. Expected: List.')
                return False
        else:
            self.error(': No input.')
            return False

    def reset(self, pin_list=None):
        """
        :param pin_list: Pins to be reseted.
        :return: Call to initialize().
        Resets the properties of the components to their defaults.
        """
        tmp_servo_list = Component.constants[self.component]['servo_list']
        tmp_motor_list = Component.constants[self.component]['motor_list']

        if tmp_servo_list or tmp_motor_list:
            if pin_list:
                if isinstance(pin_list, list):
                    if all(isinstance(command, tuple) for command in pin_list):
                        if all(len(command) == 2 for command in pin_list):
                            if all(isinstance(command[0], numbers.Number) for command in pin_list):
                                if all(isinstance(command[1], bool) for command in pin_list):
                                    pins = [command[0] for command in pin_list]
                                    initial_servos = [servo for (key, servo) in tmp_servo_list if servo["pin"] in pins]
                                    initial_motors = [motor for (key, motor) in tmp_motor_list if motor["pin"] in pins]

                                    if initial_servos:
                                        for servo_to_reset in self.servos:
                                            initial_servo = next(servo for (key, servo) in initial_servos if
                                                                 servo["pin"] == servo_to_reset.pin)

                                            if initial_servo:
                                                self.servos.remove(servo_to_reset)
                                                self.servos.append(ServoMotor(initial_servo['dependencies'],
                                                                              initial_servo['pin'],
                                                                              initial_servo['max_pulse'],
                                                                              initial_servo['min_pulse'],
                                                                              initial_servo['abs_max_pulse'],
                                                                              initial_servo['abs_min_pulse'],
                                                                              initial_servo['pulse_width'],
                                                                              initial_servo['init_pulse']))
                                    if initial_motors:
                                        for motor_to_reset in self.motors:
                                            initial_motor = next(motor for (key, motor) in initial_motors if
                                                                 motor["pin"] == motor_to_reset.pin)

                                            if initial_motor:
                                                self.motors.remove(motor_to_reset)
                                                self.motors.append(GearedMotor(initial_motor['pin'],
                                                                               initial_motor['init_percentage'],
                                                                               initial_motor['init_direction'],
                                                                               initial_motor['pulse_width']))
                                    if initial_servos or initial_motors:
                                        return self.initialize()
                                    else:
                                        self.error('No servo or motor list available.')
                                        return False
                                else:
                                    self.error('Unexpected tuple element. Second element must be a boolean.')
                                    return False
                            else:
                                self.error('Unexpected tuple element. First element must be a number')
                                return False
                        else:
                            self.error('Unexpected tuple size. Expected tuple of two')
                            return False
                    else:
                        self.error('Unexpected list element. Expected list of strings')
                        return False
                else:
                    self.error('Unexpected input: ' + type(pin_list).__name__ + '. Expected: None or List.')
                    return False
            else:
                if tmp_servo_list:
                    del self.servos[:]
                    self.servos = [ServoMotor(value['dependencies'],
                                              value['pin'],
                                              value['max_pulse'],
                                              value['min_pulse'],
                                              value['abs_max_pulse'],
                                              value['abs_min_pulse'],
                                              value['pulse_width'],
                                              value['init_pulse']) for (key, value) in tmp_servo_list.items()]

                if tmp_motor_list:
                    del self.motors[:]
                    self.motors = [GearedMotor(value['pin'],
                                               value['transmission'],
                                               value['gradation'],
                                               value['pulse_width']) for (key, value) in tmp_motor_list.items()]

                return self.initialize()
        else:
            self.error('No motor and servo information could be found in constant.json')
            return False

    def initialize(self, init_list=None):
        """
        :param init_list: List of pins to be initialized.
        :return: Call to init_command().
        Initializes the robot.
        """
        if init_list:
            return self.init_command(init_list)
        else:
            pins_to_initialize = []

            if self.servos:
                pins_to_initialize.extend([(servo.pin, False) for servo in self.servos])
            if self.motors:
                pins_to_initialize.extend([(motor.pin, False) for motor in self.motors])
            if not pins_to_initialize:
                self.error('Neither servo-list nor motor-list found.')
                return False

            return self.init_command(pins_to_initialize)

    def move_servo(self, command_list):
        """
        :param command_list: List of commands to be executed.
        :return: True for successful execution.
        Move servos according to the command_list.
        """
        if self.servos:
            if isinstance(command_list, list):
                if all(isinstance(command, tuple) for command in command_list):
                    if all(len(command) == 3 for command in command_list):
                        if all(isinstance(number, numbers.Number) for command in command_list for number in
                               command[:1]):
                            if all(isinstance(command[2], bool) for command in command_list):
                                for command in command_list:
                                    pin = command[0]
                                    degree = command[1]
                                    servo = next(servo for servo in self.servos if servo.pin == pin)

                                    if servo:
                                        if servo.min_pulse <= degree <= servo.max_pulse:
                                            if command[2]:
                                                if Controller.execute_servo(servo, degree):
                                                    self.error('Execution of single command was successfull')
                                                else:
                                                    self.error('Execution of single command failed')
                                                    return False
                                            else:
                                                if Controller.add_servo_to_stack(servo, degree):
                                                    self.error('Command was added to Execution-list.')
                                                else:
                                                    self.error('Command could not be added to Execution-list.')
                                                    return False
                                        else:
                                            self.error(str(degree) + ' is not allowed.')
                                            return False
                                    else:
                                        self.error('Desired servo with pin ' + str(pin) + ' is not available.')
                                        return False

                                return True

                            else:
                                self.error('Unexpected tuple element. Last Element must be a boolean.')
                                return False
                        else:
                            self.error('Unexpected tuple element. First two items must be numbers')
                            return False
                    else:
                        self.error('Unexpected tuple size. Expected tuple of three')
                        return False
                else:
                    self.error('Unexpected list element. Expected list of tuples')
                    return False
            else:
                self.error('Unexpected input: ' + type(command_list).__name__ + '. Expected: list')
                return False
        else:
            self.error('Component does not contain any servos.')
            return False

    def move_motor(self, command_list):
        """
        :param command_list: List of commands to be executed.
        :return: True for successful execution.
        Moves motor according to command_list.
        """
        if self.motors:
            if isinstance(command_list, list):
                if all(isinstance(command, tuple) for command in command_list):
                    if all(len(command) == 4 for command in command_list):
                        if all(isinstance(number, numbers.Number) for command in command_list for number in
                               command[:2]):
                            if all(isinstance(command[3], bool) for command in command_list):
                                for command in command_list:
                                    pin = command[0]
                                    direction = command[1]
                                    percent = command[2]
                                    motor = next(motor for motor in self.motors if motor.pin == pin)

                                    if motor:
                                        if direction in [-1, 0, 1]:
                                            if 0 <= percent <= 100:
                                                if command[2]:
                                                    if Controller.execute_motor(motor, direction, percent):
                                                        self.error('Execution of single command was successful')
                                                    else:
                                                        self.error('Execution of single command failed')
                                                        return False
                                                else:
                                                    if Controller.add_motor_to_stack(motor, direction, percent):
                                                        self.error('Command was added to Execution-list.')
                                                    else:
                                                        self.error('Command could not be added to Execution-list.')
                                                        return False
                                            else:
                                                self.error('Invalid percentage. Percentage must be beween 0 and 100.')
                                                return False
                                        else:
                                            self.error('Invalid direction. Direction must be 1 or -1.')
                                            return False
                                    else:
                                        self.error('Desired motor with pin ' + str(pin) + ' is not available.')
                                        return False

                                return True

                            else:
                                self.error('Unexpected tuple element. Last Element must be a boolean.')
                                return False
                        else:
                            self.error('Unexpected tuple element. First three items must be of type Number.')
                            return False
                    else:
                        self.error('Unexpected tuple size. Expected tuple of three')
                        return False
                else:
                    self.error('Unexpected list element. Expected list of tuples')
                    return False
            else:
                self.error('Unexpected input: ' + type(command_list).__name__ + '. Expected: list')
                return False
        else:
            self.error('Component does not contain any motors.')
            return False

    def init_command(self, init_list):
        """
        :param init_list: The list of pins to be initialized.
        :return: True for successful execution.
        Creates the initialization command for later execution.
        """
        if isinstance(init_list, list):
            if all(isinstance(command, tuple) for command in init_list):
                if all(len(command) == 2 for command in init_list):
                    if all(isinstance(command[0], numbers.Number) for command in init_list):
                        if all(isinstance(command[1], bool) for command in init_list):
                            if self.servos:
                                for command in init_list:
                                    pin = command[0]
                                    servo = next(servo for servo in self.servos if servo.pin == pin)

                                    if servo:
                                        init_list = [command for command in init_list if command[0] != pin]

                                        if command[1]:
                                            if Controller.execute_servo(servo, servo.init_pulse):
                                                self.error('Execution of single command was successful')
                                            else:
                                                self.error('Execution of single command failed')
                                                return False
                                        else:
                                            if Controller.add_servo_to_stack(servo, servo.init_pulse):
                                                self.error('Command was added to Execution-list.')
                                            else:
                                                self.error('Command could not be added to Execution-list.')
                                                return False
                                    else:
                                        self.error('Desired servo with pin ' + str(pin) + ' is not available.')
                                        return False

                            if self.motors:
                                for command in init_list:
                                    pin = command[0]
                                    motor = next(motor for motor in self.motors if motor.pin == pin)

                                    if motor:
                                        if command[1]:
                                            if Controller.execute_motor(motor, motor.init_direction, motor.init_percentage):
                                                self.error('Execution of single command was successful')
                                            else:
                                                self.error('Execution of single command failed')
                                                return False
                                        else:
                                            if Controller.add_motor_to_stack(motor, motor.init_direction, motor.init_percentage):
                                                self.error('Command was added to Execution-list.')
                                            else:
                                                self.error('Command could not be added to Execution-list.')
                                                return False
                                    else:
                                        self.error('Desired motor with pin ' + str(pin) + ' is not available.')
                                        return False

                            if self.servos or self.motors:
                                return True
                            else:
                                self.error('No servo or motor list available.')
                                return False
                        else:
                            self.error('Unexpected tuple element. Second element must be a boolean.')
                            return False
                    else:
                        self.error('Unexpected tuple element. First element must be a number')
                        return False
                else:
                    self.error('Unexpected tuple size. Expected tuple of two')
                    return False
            else:
                self.error('Unexpected list element. Expected list of tuples')
                return False
        else:
            self.error('Unexpected input: ' + type(init_list).__name__ + '. Expected: list')
            return False

    def error(self, string):
        """
        :param string: Error to be displayed.
        :return: Call to print() with error message.
        Error output method.
        """
        print(self.component + ': ' + string)