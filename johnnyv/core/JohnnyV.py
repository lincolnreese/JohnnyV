import json
from johnnyv.core.Component import Component
from johnnyv.core.Camera import Camera
from johnnyv.core.SRF08 import SRF08
from johnnyv.core.Controller import Controller
from johnnyv.core.RaspberryPi import RaspberryPi


class JohnnyV:
    """
    Core class of JohnnyV robot.
    """
    constants = json.load(open('/home/link//JohnnyV/johnnyv/ext/Constants.json'))

    def __init__(self):
        self.components = {key: Component(key) for (key, value) in self.constants['components'].items()}
        self.peripherals = {key: Camera(key) for (key, value) in self.constants['cameras'].items()}
        self.peripherals.update({key: SRF08(key) for (key, value) in self.constants['sensors'].items()})
        self.controller = Controller()

    def initialize(self):
        """
        :return: True for successful initialization.

        Initializes the robot, e.g setts all servos to initial pulse.
        """
        try:
            JohnnyV.validate_results([value.initialize() for (key, value) in self.components.items()], 'Initialization')
            return True
        except:
            print("Initialization error!")
            raise

    def reset(self):
        """
        :return: True for successful reset.

        Resets the robot, e.g setts all components to their standards.
        """
        try:
            JohnnyV.validate_results([value.reset() for (key, value) in self.components.items()], 'Reset')
            return True
        except:
            print("Reset error!")
            raise

    @staticmethod
    def validate_results(feedback_list, method):
        """
        :param feedback_list: List of booleans corresponding to the return value of a method.
        :param method: Method name, i.e initialize.
        :return: True if all booleans in feedback_list are True.

        Validates results of executed method and executes stack.
        """
        if False not in feedback_list:
            Controller.execute_stack()
            print('JohnnyV: ' + method + ' was successful.')
            return True
        else:
            print('JohnnyV: ' + method + ' failed. Commands could not be written to SSC board.')
            return False

    @staticmethod
    def execute_stack():
        """
        :return: True for successful execution.

        Parallel execution of pending commands on the SSC32U board.
        """
        try:
            Controller.execute_stack()
            return True
        except:
            print("Executing stack failed!")
            raise

    def dab(self):
        head = self.components['head']
        base = self.components['base']
        back = self.components['back']
        left_arm = self.components['left_arm']
        right_arm = self.components['right_arm']

        # Head
        head.move_servo([(29, 153, False)])

        # Base
        base.move_servo([(16, 99, False)])

        # Back
        back.move_servo([(17, 90, False), (18, 108, False)])

        # LeftArm
        left_arm.move_servo([(19, 90, False), (20, 81, False), (21, 90, False),
                             (22, 90, False), (23, 63, False)])

        # RightArm
        right_arm.move_servo([(24, 0, False), (25, 9, False), (26, 90, False),
                              (27, 18, False), (28, 114, False)])

        # Execute
        self.execute_stack()

    def praise_the_lord(self):
        head = self.components['head']
        base = self.components['base']
        back = self.components['back']
        left_arm = self.components['left_arm']
        right_arm = self.components['right_arm']

        # Head
        head.move_servo([(29, 90, False)])

        # Base
        base.move_servo([(16, 90, False)])

        # Back
        back.move_servo([(17, 90, False), (18, 72, False)])

        # LeftArm
        left_arm.move_servo([(19, 180, False), (20, 180, False), (21, 90, False),
                             (22, 90, False), (23, 63, False)])

        # RightArm
        right_arm.move_servo([(24, 8, False), (25, 0, False), (26, 90, False),
                              (27, 90, False), (28, 114, False)])

        # Execute
        self.execute_stack()

        # LeftArm
        left_arm.move_servo([(23, 180, False)])

        # RightArm
        right_arm.move_servo([(28, 0, False)])

        # Execute
        self.execute_stack()

        # LeftArm
        left_arm.move_servo([(23, 63, False)])

        # RightArm
        right_arm.move_servo([(28, 114, False)])

        # Execute
        self.execute_stack()

        # LeftArm
        left_arm.move_servo([(23, 180, False)])

        # RightArm
        right_arm.move_servo([(28, 0, False)])

        # Execute
        self.execute_stack()

    def running_man(self):
        left_arm = self.components['left_arm']
        right_arm = self.components['right_arm']
        track = self.components['track']

        # LeftArm
        left_arm.move_servo([(19, 135, False), (22, 90, False)])

        # RightArm
        right_arm.move_servo([(24, 129, False), (27, 90, False)])

        # Track
        track.move_motor([(31, 1, 50, False)])

        # Execute
        self.execute_stack()

        # LeftArm
        left_arm.move_servo([(19, 54, False), (22, 90, False)])

        # RightArm
        right_arm.move_servo([(24, 45, False), (27, 90, False)])

        # Execute
        self.execute_stack()

        # LeftArm
        left_arm.move_servo([(19, 135, False), (22, 90, False)])

        # RightArm
        right_arm.move_servo([(24, 129, False), (27, 90, False)])

        # Execute
        self.execute_stack()

        # LeftArm
        left_arm.move_servo([(19, 54, False), (22, 90, False)])

        # RightArm
        right_arm.move_servo([(24, 45, False), (27, 90, False)])

        # Execute
        self.execute_stack()

        track.move_motor([(31, 0, 0, True)])


