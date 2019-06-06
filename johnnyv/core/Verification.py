import json
from jsonschema import Draft4Validator, FormatChecker
from jsonschema.exceptions import best_match


class Verification:
    constants = json.load(open('/home/pi/johnnyv/ext/Constants.json'))
    conSchema = json.load(open('/home/pi/johnnyv/ext/Schema.json'))

    @staticmethod
    def validate():
        result = best_match(Draft4Validator(Verification.conSchema,
                                            format_checker=FormatChecker()).iter_errors(Verification.constants))

        if result:
            index_range = len(list(result.schema_path))

            if index_range > 4:
                print("FAILURE: " + list(result.schema_path)[4], result.message, sep=", ")
                return False

            elif index_range == 4:
                print("FAILURE: " + list(result.schema_path)[3], result.message, sep=", ")
                return False

            elif index_range == 3:
                print("FAILURE: " + list(result.schema_path)[2], result.message, sep=", ")
                return False

            elif index_range == 2:
                print("FAILURE: " + list(result.schema_path)[1], result.message, sep=", ")
                return False

            else:
                print("FAILURE: " + list(result.schema_path)[0], result.message, sep=", ")
                return False
        else:
            servo_lists = [value["servo_list"] for (key, value) in Verification.constants['components'].items()]
            motor_lists = [value["motor_list"] for (key, value) in Verification.constants['components'].items()]
            servo_pins = [value["pin"] for group in servo_lists for (key, value) in group.items()]
            motor_pins = [value["pin"] for group in motor_lists for (key, value) in group.items()]

            if len(servo_pins + motor_pins) == len(set(servo_pins + motor_pins)):
                for (key, value) in Verification.constants['components'].items():
                    servo_schemes = [value["color_scheme"] for (key, value) in value["servo_list"].items()]
                    motor_schemes = [value["color_scheme"] for (key, value) in value["motor_list"].items()]

                    if not len(servo_schemes + motor_schemes) == len(set(servo_schemes + motor_schemes)):
                        print("FAILURE: Multiple use of a color-scheme in one component.")
                        return False

                print("Validation of 'constants.json' was successful.")
                return True

            else:
                print("FAILURE: Pins are double used.")
                return False
