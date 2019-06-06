import json
from johnnyv.core.Controller import Controller


class SRF08:
    """
    Ultrasonic ranger (range-finder) with light sensor
    """

    constants = json.load(open('/home/link//JohnnyV/johnnyv/ext/Constants.json'))

    def __init__(self, sensor_id):
        """
        :param sensor_id: ID/Name of sensor.
        """
        self.sensor_id = sensor_id
        self.sensor_specs = SRF08.constants['sensors'][sensor_id]

        if self.sensor_specs:
            self.sensor_addr = Controller.get_sensor_addr()
            self.unit = self.sensor_specs["unit"]
            self.unit_set = self.sensor_specs["unit_set"]
        else:
            print(self.sensor_id+": No specifications found for given Sensor-ID.")

    def write(self, unit=None):
        """
        :param unit: Unit of measurement, i.e 'inches'. Standard is on 'centimeter'.
        :return: Call to Controller.write_to_sensor().

        Method to write commands to sensor.
        """
        if unit is None:
            return Controller.write_to_sensor(self, self.unit)
        else:
            if isinstance(unit, str):
                if unit in self.unit_set:
                    return Controller.write_to_sensor(self, unit)
                else:
                    print("Camera: Measure Range must be in " + self.unit_set)
                    return False
            else:
                print("Camera: Measure Range must be a string).")
                return False

    def light_level(self):
        """
        :return: Call to Controller.light_level().

        Method for reading current light level of SRF08 sensor.
        """
        return Controller.light_level(self)

    def range(self):
        """
        :return: Call to Controller.sensor_range().

        Method to return raw range of SRF08 sensor.
        """
        return Controller.sensor_range(self)

    def measure_range(self, unit=None):
        """
        :param unit: Unit of measurement, i.e 'inches'. Standard is on 'centimeter'.
        :return: Call to Controller.measure_range().

        Method for returning aggregated range.
        """
        if unit is None:
            return Controller.measure_range(self, self.unit)
        else:
            if isinstance(unit, str):
                if unit in self.unit_set:
                    return Controller.measure_range(self, unit)
                else:
                    print("Camera: Measure Range must be in " + self.unit_set)
                    return False
            else:
                print("Camera: Measure Range must be a string).")
                return False