from unittest import TestCase

from johnnyv.core.SSC32U import SSC32U


class TestSSC32U(TestCase):

    def test_initialize(self):
        self.fail()

    def test_set_port(self):
        ser = SSC32U()
        ser.set_port("UnitTest")
        self.assertEqual(ser.port, "UnitTest")

    def test_set_baud(self):
        ser = SSC32U()
        ser.set_baud(9999)
        self.assertEqual(ser.baud, 9999)

    def test_set_timeout(self):
        ser = SSC32U()
        ser.set_timeout(9.9)
        self.assertEqual(ser.port, 9.9)

    def test_check_connection(self):
        ser = SSC32U()
        self.assertTrue(ser.check_connection())

    def test_is_done(self):
        self.fail()

    def test_get_baud(self):
        self.fail()

    def test_get_val_from_reg(self):
        self.fail()

    def test_reset_reg_vals(self):
        self.fail()

    def test_get_startup_string(self):
        self.fail()

    def test_stop_servo(self):
        self.fail()

    def test_exec_command(self):
        self.fail()

    def test_is_closed(self):
        self.fail()

