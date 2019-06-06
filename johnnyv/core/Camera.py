import re
import json
from johnnyv.core.Controller import Controller


class Camera:
    """
    RaspberryPi compatible camera
    """

    constants = json.load(open('/home/link/JohnnyV/johnnyv/ext/Constants.json'))

    def __init__(self, camera_id):
        """
        :param camera_id: ID/Name of camera.
        """
        self.camera_id = camera_id
        self.camera_specs = Camera.constants['cameras'][camera_id]

        if self.camera_specs:
            self.resolution = self.camera_specs["resolution"]
            self.resolution_set = self.camera_specs["resolution_set"]
            self.brightness = self.camera_specs["brightness"]
            self.contrast = self.camera_specs["contrast"]
            self.sharpness = self.camera_specs["sharpness"]
            self.saturation = self.camera_specs["saturation"]
            self.rotation = self.camera_specs["rotation"]
            self.hflip = self.camera_specs["hflip"]
            self.vflip = self.camera_specs["vflip"]
            self.picture_extension = self.camera_specs["picture_extension"]
            self.video_extension = self.camera_specs["video_extension"]
            self.picture_path = self.camera_specs["picture_path"]
            self.video_path = self.camera_specs["video_path"]
        else:
            print(self.camera_id+": No specifications found for given Camera-ID.")

    def capture(self, file_name):
        """
        :param file_name: Name of the picture that will be taken without extension.
        :return: Call to Controller.capture().

        Creates a picture with given filename.
        """
        if isinstance(file_name, str):
            pattern = re.compile("^([a-zA-Z0-9]+)$")
            if pattern.match(file_name):
                return Controller.capture(self, file_name)
            else:
                print("Camera: File_name does not fit pattern: ^([a-zA-Z0-9]+)$")
                return False
        else:
            print("Camera: File_name must be a string.")
            return False

    def record(self, file_name, duration):
        """
        :param file_name: Name of the video that will be taken without extension.
        :param duration: Recording time.
        :return: Call to Controller.record().

        Creates a video with given filename.
        """
        if isinstance(file_name, str):
            pattern = re.compile("^([a-zA-Z0-9]+)$")
            if pattern.match(file_name):
                if isinstance(duration, int) and duration > 0:
                    return Controller.record(self, file_name, duration)
                else:
                    print("Camera: Duration must be a integer greater 0.")
                    return False
            else:
                print("Camera: File_name does not fit pattern: ^([a-zA-Z0-9]+)$")
                return False
        else:
            print("Camera: File_name must be a string.")
            return False

    def set_resolution(self, resolution):
        """
        :param resolution: The value to be set to the resolution.
        :return: True if value was set successfully.

        Method to set new resolution value to videos or pictures.
        """
        if isinstance(resolution, str):
            if resolution in self.resolution_set:
                self.resolution = resolution
                return True
            else:
                print("Camera: Resolution must be in "+self.resolution_set)
                return False
        else:
            print("Camera: Resolution must be a string (WIDTHxHIGHT).")
            return False

    def set_brightness(self, brightness):
        """
        :param brightness: The value to be set to the brightness.
        :return: True if value was set successfully.

        Method to set new brightness value to videos or pictures.
        """
        if isinstance(brightness, int):
            if 0 <= brightness <= 100:
                self.brightness = brightness
                return True
            else:
                print("Camera: Brightness must be in range of 0 and 100.")
                return False
        else:
            print("Camera: Brightness must be an integer.")
            return False

    def set_contrast(self, contrast):
        """
        :param contrast: The value to be set to the contrast.
        :return: True if value was set successfully.

        Method to set new contrast value to videos or pictures.
        """
        if isinstance(contrast, int):
            if -100 <= contrast <= 100:
                self.brightness = contrast
                return True
            else:
                print("Camera: Contrast must be in range of -100 and 100.")
                return False
        else:
            print("Camera: Contrast must be an integer.")
            return False

    def set_sharpness(self, sharpness):
        """
        :param sharpness: The value to be set to the sharpness.
        :return: True if value was set successfully.

        Method to set new sharpness value to videos or pictures.
        """
        if isinstance(sharpness, int):
            if -100 <= sharpness <= 100:
                self.saturation = sharpness
                return True
            else:
                print("Camera: Sharpness must be in range of -100 and 100.")
                return False
        else:
            print("Camera: Sharpness must be an integer.")
            return False

    def set_saturation(self, saturation):
        """
        :param saturation: The value to be set to the saturation.
        :return: True if value was set successfully.

        Method to set new saturation value to videos or pictures.
        """
        if isinstance(saturation, int):
            if -100 <= saturation <= 100:
                self.saturation = saturation
                return True
            else:
                print("Camera: Saturation must be in range of -100 and 100.")
                return False
        else:
            print("Camera: Saturation must be an integer.")
            return False

    def set_rotation(self, rotation):
        """
        :param rotation: Degree of picture/video rotation.
        :return: True if value was set successfully.

        Method to set new rotation value to videos or pictures.
        """
        if isinstance(rotation, int):
            if rotation in [0, 90, 180, 270]:
                self.rotation = rotation
                return True
            else:
                print("Camera: Rotation must be 0, 90, 180 or 270.")
                return False
        else:
            print("Camera: Rotation must be an integer.")
            return False

    def set_hflip(self, h_flip):
        """
        :param h_flip: Adding a horizontal flip to camera. True for flip.
        :return: True if value was set successfully.

        Method to set new h_flip value to camera.
        """
        if isinstance(h_flip, bool):
            self.hflip = h_flip
            return True
        else:
            print("Camera: Hflip must be a boolean.")
            return False

    def set_vflip(self, v_flip):
        """
        :param v_flip: Adding a vertical flip to camera. True for flip.
        :return: True if value was set successfully.

        Method to set new v_flip value to camera.
        """
        if isinstance(v_flip, bool):
            self.vflip = v_flip
            return True
        else:
            print("Camera: V_flip must be a boolean.")
            return False

    def set_picture_path(self, path):
        """
        :param path: Pictures will be saved under given path.
        :return: True if value was set successfully.

        Method to set new picture path.
        """
        if isinstance(path, str):
            pattern = re.compile("^(/[a-zA-Z0-9]+)+$")
            if pattern.match(path):
                self.picture_path = path
                return True
            else:
                print("Camera: Path does not fit pattern: ^(/[a-zA-Z0-9]+)+$")
                return False
        else:
            print("Camera: Path must be a string.")
            return False

    def set_video_path(self, path):
        """
        :param path: Videos will be saved under given path.
        :return: True if value was set successfully.

        Method to set new video path.
        """
        if isinstance(path, str):
            pattern = re.compile("^(/[a-zA-Z0-9]+)+$")
            if pattern.match(path):
                self.video_path = path
                return True
            else:
                print("Camera: Path does not fit pattern: ^(/[a-zA-Z0-9]+)+$")
                return False
        else:
            print("Camera: Path must be a string.")
            return False
