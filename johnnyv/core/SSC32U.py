import json
import serial
import time
from johnnyv.core.RaspberryPi import RaspberryPi


class SSC32U:
    """
    Lynxmotion USB servo controller board
    Specs:
    Voltage: 6V
    Baud rates: 9600 (green LED), 38400 (red LED), 115200 (greed red LED)
    Full specs: https://www.robotshop.com/media/files/pdf2/lynxmotion_ssc-32u_usb_user_guide.pdf
    """

    def __init__(self):
        settings = json.load(open('/home/link/JohnnyV/johnnyv/ext/Constants.json'))["ssc32u"]
        self.port = "/dev/ttyUSB0" #RaspberryPi.get_usb_port()
        self.baud = settings["baud"]
        self.timeout = settings["timeout"]
        self.execution_time = settings["execution_time"]
        self.ser = SSC32U.initialize(self)

    def initialize(self):
        """
        :return: Returns an instance of the initialized serial connection.

        Method for initializing a SSC32U board serial connection.
        """
        try:
            ser = serial.Serial(port=self.port, baudrate=self.baud, timeout=self.timeout)
            return ser
        except serial.SerialException:
            print("SSC32U initialization failed. Check parameters!")
            raise

    def set_execution_time(self, execution_time):
        """
        :param execution_time: Time the execution needs to execute given commands.

        Method for setting the execution time of the serial connection.
        """
        self.execution_time = execution_time

    def set_port(self, port):
        """
        :param port: The value to be set to the port of the serial connection.

        Method for setting the port of the serial connection.
        """
        self.port = port

    def set_baud(self, baud):
        """
        :param baud: The value to be set to the baud rate of the serial connection.

        Method for setting the baud rate of the serial connection.
        """
        self.baud = baud

    def set_timeout(self, timeout):
        """
        :param timeout: The value to be set to the timeout of the serial connection.

        Method for setting the timeout of the serial connection.
        """
        self.timeout = timeout

    def check_connection(self):
        """
        :return: True if the connection was successful, False otherwise.

        Checks connection to the SSC32-U board.
        """
        if SSC32U.is_closed(self):
            try:
                self.ser.open()

                if self.ser.read(self.ser.write('R0 \r'.encode())).decode() != "":
                    return True
                else:
                    return False
            except serial.SerialException:
                raise
            finally:
                self.ser.close()
        else:
            print('Error closing serial!')

    def is_done(self):
        """
        :return: True if previous command are done, False otherwise.

        Method for checking if the serial connection is done executing previous commands.
        """
        if SSC32U.is_closed(self):
            try:
                self.ser.open()
                result = self.ser.read(self.ser.write('Q \r'.encode())).decode()

                # Result '.' if previous move is completed
                return result == '.'
            except serial.SerialException:
                raise
            finally:
                self.ser.close()
        else:
            print('Error closing serial!')

    def get_baud(self):
        """
        :return: The value of the baud rate.

        Get current baud rate.
        """
        if SSC32U.is_closed(self):
            try:
                self.ser.open()
                return self.ser.read(self.ser.write('R4 \r'.encode())).decode()
            except serial.SerialException:
                raise
            finally:
                self.ser.close()
        else:
            print('Error closing serial!')

    def get_val_from_reg(self, reg):
        """
        :param reg: The register to get the value from.
        :return: The value of the register.

        Get value from of given register.
        Allowed registers:
        Register 1: TransmitDelay
        Register 2: TransmitPacing
        Register 32-63: InitialPulseOffset (32=>servo #0, 33=>servo #1....)
        Register 64-95: InitialPulseWidth  (64=>servo #0, 65=>servo #1....)
        """
        if SSC32U.is_closed(self):
            try:
                self.ser.open()
                return self.ser.read(self.ser.write(('R ' + str(reg) + ' \r').encode())).decode()
            except serial.SerialException:
                raise
            finally:
                self.ser.close()
        else:
            print('Error closing serial!')

    def reset_reg_vals(self):
        """
        :return: Call to serial.read() method.

        Method for restoring the default values of all registers.
        """
        if SSC32U.is_closed(self):
            try:
                self.ser.open()
                return self.ser.read(self.ser.write('RDFLT \r'.encode())).decode()
            except serial.SerialException:
                raise
            finally:
                self.ser.close()
        else:
            print('Error closing serial!')

    def get_startup_string(self):
        """
        :return: Value of startup string.

        Get startup string.
        """
        if SSC32U.is_closed(self):
            try:
                self.ser.open()
                return self.ser.read(self.ser.write('SS \r'.encode())).decode()
            except serial.SerialException:
                raise
            finally:
                self.ser.close()
        else:
            print('Error closing serial!')

    def stop_servo(self, pin):
        """
        :param pin: The pin of the servo to be stopped.
        :return: True for successful stopping, False otherwise.

        Method that stops the servo on pin 'pin' at its current position.
        """
        if SSC32U.is_closed(self):

            try:
                self.ser.open()
                self.ser.write(('STOP ' + pin + ' \r').encode())
                return True
            except serial.SerialException:
                raise
            finally:
                self.ser.close()
        else:
            print('Error closing serial!')

    def exec_command(self, parameters):
        """
        :param parameters: A list with the following format = ['pin:pulse:time', 'pin:pulse:time', .....].
        :return: True for successful execution, False otherwise.

        #Pin   => '#' followed by the pin number (no spaces).
        Ppulse => 'P' followed by the pulse width (no spaces).*
        Ttime  => 'T' followed by the time in microseconds for executing the pulse (no spaces).
        \r => all commands end with a carriage return.
        *Pulse width from 500-2500 (1500 <=> 0°, 500 <=> 0°, 2500 <=> +180°).
        Execute command on servo.
        """
        if parameters and parameters is not None:
            if SSC32U.is_closed(self):
                data = ''
                for elem in parameters:
                    pin = ' #' + elem.split(':')[0]
                    pulse_width = ' P' + elem.split(':')[1]
                    pulse_time = ' T' + elem.split(':')[2]
                    data += pin + pulse_width + pulse_time

                data += ' \r'
                print(data)
                try:
                    self.ser.open()
                    self.ser.write(data.encode())
                    time.sleep(self.execution_time)
                    return True
                except serial.SerialException:
                    raise
                finally:
                    self.ser.close()
            else:
                print('Error closing serial!')

    def is_closed(self):
        """
        :return: Return True if connection is closed, Return True if connection is open after closing it.

        Check serial connection status
        """
        if self.ser.isOpen():
            try:
                self.ser.close()
                return True
            except serial.SerialException:
                raise
        else:
            return True

    def to_string(self):
        return "" + self.port + "," + self.baud + "," + self.timeout
