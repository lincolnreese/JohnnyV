from johnnyv.core.SSC32U import SSC32U
from johnnyv.core.RaspberryPi import RaspberryPi
from johnnyv.core.Observer import Observer


class Controller:
    """
    Interface between components and control boards.
    """

    ssc32u = SSC32U()
    raspberryPi = RaspberryPi()
    execution_list = []
    servos_to_notify = []

    # Observable methods
    @staticmethod
    def add_servos(list_of_observers):
        """
        :param list_of_observers: List of Observers which should be added.
        :return: True for successful adding.

        Method adds Observers to the servos_to_notify list.
        """
        if isinstance(list_of_observers, list):
            if all(isinstance(observer, Observer) for observer in list_of_observers):
                for single_observer in list_of_observers:
                    if single_observer not in Controller.servos_to_notify:
                        Controller.servos_to_notify.append(single_observer)
                return True
            else:
                print("Controller: Unexpected list element. Expected list of Observer")
                return False
        else:
            print('Controller: Unexpected input: ' + type(list_of_observers).__name__ + '. Expected: list')
            return False

    @staticmethod
    def remove_servos(observer):
        """
        :param observer: Observer object that should be removed.
        :return: True for successful removing.

        Removes given observer from list.
        """
        if observer in Controller.servos_to_notify:
            Controller.servos_to_notify.remove(observer)
            return True
        else:
            return False

    @staticmethod
    def remove_all_servos():
        """
        :return: True for successful removing, False if a failure occurred.

        Removes all servomotors from the servos_to_notify list.
        """
        if Controller.servos_to_notify:
            del Controller.servos_to_notify[:]
            return True
        else:
            return False

    @staticmethod
    def update_servo_information(pin, degree):
        """
        :param pin: Pin of recently moved servomotor.
        :param degree: Degree of Movement.
        :return: True for successful updating.

        Hands over changed servomotor-information to every servomotor in servos_to_notify.
        """
        for servos in Controller.servos_to_notify:
            servos.update(pin, degree)

        return True

    # Servomotor and gearedmotor methods
    @staticmethod
    def execute_stack():
        """
        :return: True for successful execution.

        Executes all commands in execution stack.
        """
        if Controller.ssc32u.exec_command(Controller.execution_list):
            del Controller.execution_list[:]
            return True
        else:
            del Controller.execution_list[:]
            return False

    @staticmethod
    def add_to_stack(command):
        """
        :param command: Command to be stored in execution list.
        :return: True for successful execution.

        Adds commands to execution_stack.
        """
        if Controller.check_commands(command):
            Controller.execution_list.extend(command)
            return True
        else:
            return False

    @staticmethod
    def add_servo_to_stack(servo, degree):
        """
        :param servo: Desired servomotor.
        :param degree: Desired degree.
        :return: Call to add_to_stack().

        Adds a servo movement to the execution stack.
        """
        command = [Controller.get_servo_command(servo, degree)]
        return Controller.add_to_stack(command)

    @staticmethod
    def add_motor_to_stack(motor, direction, percentage):
        """
        :param motor: Desired motor.
        :param direction: Desired direction.
        :param percentage: Desired PWM in percentage.
        :return: Call to add_to_stack().

        Add a motor movement to the execution stack.
        """
        command = [Controller.get_motor_command(motor, direction, percentage)]
        return Controller.add_to_stack(command)

    @staticmethod
    def direct_execute(command):
        """
        :param command: Command to be executed.
        :return: True for successful execution.

        Directly executes given command.
        """
        if Controller.check_commands(command):
            if Controller.ssc32u.exec_command(command):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def execute_servo(servo, degree):
        """
        :param servo: Desired servo.
        :param degree: Desired degree.
        :return: True for successful execution.

        Execute command with degree on servomotor.
        """
        command = [Controller.get_servo_command(servo, degree)]

        if Controller.direct_execute(command):
            Controller.update_servo_information(servo.pin, degree)
            return True
        else:
            return False

    @staticmethod
    def execute_motor(motor, direction, percentage):
        """
        :param motor: Desired motor.
        :param direction: Desired direction.
        :param percentage: Desire percentage.
        :return: Call to direct_execute().

        Execute command with direction and percentage on motor.
        """
        command = [Controller.get_motor_command(motor, direction, percentage)]
        return Controller.direct_execute(command)

    @staticmethod
    def convert_degree(degree):
        """
        :param degree: Degree to be converted.
        :return: Converted degree.

        Convert degree to pulse.
        """
        return str(int(500 + (100 / 9) * int(degree)))

    @staticmethod
    def convert_pulse_width(current_position, degree, pulse_span, pulse_width):
        """
        :param current_position: Last known servo position.
        :param degree: Desired degree movement of servo.
        :param pulse_span: Allowed span for servo movement.
        :param pulse_width: Default pulse width of servomotor.
        :return: Converted pulse width.

        Compute optimal pulse width for desired servo action.
        """
        if current_position == degree:
            return str(pulse_width)
        else:
            return str(int((abs(current_position - degree) / pulse_span) * pulse_width))

    @staticmethod
    def check_commands(command_list):
        """
        :param command_list: List of commands to be checked.
        :return: True if all commands are Ok.

        Checks the integrity of the command list.
        """
        if isinstance(command_list, list):
            if all(isinstance(string, str) for string in command_list):
                if all(command.count(':') == 2 for command in command_list):
                    for command in command_list:
                        split_command = command.split(':')

                        pin = split_command[0]
                        degree = split_command[1]
                        time = split_command[2]

                        if pin.isdigit():
                            if degree.isdigit():
                                if not time.isdigit():
                                    print("Controller: Unexpected input: " + time + ". Expected: 'number'")
                                    return False
                            else:
                                print("Controller: Unexpected input: " + degree + ". Expected: 'number'")
                                return False
                        else:
                            print("Controller: Unexpected input: " + pin + ". Expected: 'number'")
                            return False

                    return True

                else:
                    print("Controller: Input does not fit command pattern. Too many ':' were found")
                    return False
            else:
                print("Controller: Unexpected list element. Expected list of strings")
                return False
        else:
            print(command_list)
            print("Controller: Unexpected input: " + type(command_list).__name__ + ". Expected: list")
            return False

    @staticmethod
    def get_servo_command(servo, degree):
        """
        :param servo: Servo to create the command for.
        :param degree: Degree to which the servo should move.
        :return: Servo command.

        Creates a servo movement command according to the degree given.
        """
        return '{0}:{1}:{2}'.format(str(servo.pin), Controller.convert_degree(degree),
                                    Controller.convert_pulse_width(servo.current_position,
                                                                   degree,
                                                                   servo.pulse_span,
                                                                   servo.pulse_width))

    @staticmethod
    def get_motor_command(motor, direction, percentage):
        """
        :param motor: Motor to create the command for.
        :param direction: Desired direction.
        :param percentage: Desired PWM in percentage.
        :return: Motor command.

        Create a motor movement command.
        """
        return str(motor.pin) + ':' + str(direction * (300 + 2 * percentage) + 1500) + ':1000'

    # Camera methods
    @staticmethod
    def capture(camera, file_name):
        """
        :param camera: Desired camera object.
        :param file_name: Name of file.
        :return: Call to RaspberryPi.capture().

        Creates a picture with given filename.
        """
        return RaspberryPi.capture(camera, file_name)

    @staticmethod
    def record(camera, file_name, duration):
        """
        :param camera: Desired camera object.
        :param file_name: Name of file.
        :param duration: Recording time.
        :return: Call to RaspberryPi.record().

        Creates a video with given filename.
        """
        return RaspberryPi.record(camera, file_name, duration)

    # Sensor methods
    @staticmethod
    def get_sensor_addr():
        """
        :return: Call to RaspberryPi.get_sensor_addr():

        Method for getting the address of the connected sensor.
        """
        return Controller.raspberryPi.get_sensor_addr()

    @staticmethod
    def write_to_sensor(sensor, unit):
        """
        :param sensor: Desired sensor.
        :param unit: Unit of measurement, i.e 'inches'. Standard is on 'centimeter'.
        :return: Call to RaspberryPi.write_to_sensor().

        Method to write commands to sensor.
        """
        return Controller.raspberryPi.write_to_sensor(sensor, sensor.unit_set[unit])

    @staticmethod
    def light_level(sensor):
        """
        :param sensor: Desired sensor.
        :return: Call to RaspberryPi.light_level().

        Method for reading current light level of SRF08 sensor.
        """
        return Controller.raspberryPi.light_level(sensor)

    @staticmethod
    def sensor_range(sensor):
        """
        :param sensor: Desired sensor.
        :return: Call to RaspberryPi.sensor_range().

        Method to return raw range of sensor.
        """
        return Controller.raspberryPi.sensor_range(sensor)

    @staticmethod
    def measure_range(sensor, unit):
        """
        :param sensor: Desired sensor.
        :param unit: Unit of measurement, i.e 'inches'. Standard is on 'centimeter'.
        :return: Call to RaspberryPi.measure_range().

        Method for returning aggregated range.
        """
        return Controller.raspberryPi.measure_range(sensor, sensor.unit_set[unit])
