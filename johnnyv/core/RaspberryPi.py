import os
import glob
import smbus
import time
import json
#from picamera import PiCamera


class RaspberryPi:
    """
    Raspberry Pi model 2 B single board computer
    Specs:
    900MHz quad core ARM Cortex-A7 CPU
    1GB RAM
    Full specs: https://www.raspberrypi.org/products/raspberry-pi-2-model-b/
    """

    constants = json.load(open('/home/link/JohnnyV/johnnyv/ext/Constants.json'))

    def __init__(self):
        self.rpi_specs = RaspberryPi.constants['raspberrypi']
        self.ip = self.rpi_specs["ip"]
        self.username = self.rpi_specs["username"]
        self.password = self.rpi_specs["password"]
        self.smbus = smbus.SMBus(1)

    @staticmethod
    def get_usb_port():
        """
        :return: USB port.

        Method for getting connected USB port.
        """
        return glob.glob("/dev/ttyUSB*")[0]

    @classmethod
    def get_sensor_addr(cls):
        """
        :return: Sensor address.

        Method for getting the address of the connected sensor.
        """
        i2c = os.popen("sudo i2cdetect -y 1").read().split()
        for i in range(len(i2c)):
            if i2c[i][1:3] != "0:" and i2c[i][1:2] != "":
                if i2c[i] != "--":
                    return i2c[i]

    def write_to_sensor(self, sensor, value):
        """
        :param sensor: Desired sensor.
        :param value: 0x50 for inches, 0x51 for centimeter, 0x52 for milliseconds.
        :return: Range in desired unit.

        Method for writing bytes to SRF08 sensor.
        """
        print("RaspberryPi: ")
        return self.smbus.write_byte_data(sensor.sensor_addr, 0, value)

    def light_level(self, sensor):
        """
        :param sensor: Desired sensor.
        :return: Light level.

        Method for reading current light level of SRF08 sensor.
        """
        return self.smbus.read_byte_data(sensor.sensor_addr, 1)

    def sensor_range(self, sensor):
        """
        :param sensor: Desired sensor.
        :return: Range.

        Method to return raw range of SRF08 sensor.
        """
        range1 = self.smbus.read_byte_data(sensor.sensor_addr, 2)
        range2 = self.smbus.read_byte_data(sensor.sensor_addr, 3)
        return (range1 << 8) + range2

    def measure_range(self, sensor, unit):
        """
        :param sensor: Desired sensor.
        :param unit: Desired unit of range output. Default=centimeter. Options=centimeter, inches, milliseconds
        :return: Aggregated range and current light level as dictionary or -1 as error message

        Method for returning aggregated range.
        """
        self.write_to_sensor(sensor, unit)
        time.sleep(0.07)
        light_level = self.light_level(sensor)
        ranges = [self.sensor_range(sensor)]

        return {'range:': int(sum(ranges) / len(ranges)), 'light level:': light_level}

    @staticmethod
    def capture(camera, file_name):
        """
        :param camera: Desired camera.
        :param file_name: Name of the picture that will be taken without extension.
        :return: True for successful capture, False otherwise.

        Method for capturing a picture.
        """
        try:
            with PiCamera() as pi_camera:
                pi_camera.resolution = camera.resolution
                pi_camera.brightness = camera.brightness
                pi_camera.contrast = camera.contrast
                pi_camera.sharpness = camera.sharpness
                pi_camera.saturation = camera.saturation
                pi_camera.rotation = camera.rotation
                pi_camera.hflip = camera.hflip
                pi_camera.vflip = camera.vflip

                pi_camera.capture(camera.picture_path + "/" + file_name + camera.picture_extension)
                return True

        except Exception:
            print('Error capturing picture!')
            raise

    @staticmethod
    def record(camera, file_name, duration):
        """
        :param camera: Desired camera.
        :param file_name: Name of the picture that will be taken without extension.
        :param duration: Duration of the video that will be taken in seconds.
        :return: True for successful recording, False otherwise.

        Method for recording a video.
        """
        try:
            with PiCamera() as pi_camera:
                pi_camera.resolution = camera.resolution
                pi_camera.brightness = camera.brightness
                pi_camera.contrast = camera.contrast
                pi_camera.sharpness = camera.sharpness
                pi_camera.saturation = camera.saturation
                pi_camera.rotation = camera.rotation
                pi_camera.hflip = camera.hflip
                pi_camera.vflip = camera.vflip

                pi_camera.start_recording(camera.video_path + "/" + file_name + camera.video_extension)

                time.sleep(duration)

                pi_camera.camera.stop_recording()
                return True

        except Exception:
            print('Error recording video!')
            raise
