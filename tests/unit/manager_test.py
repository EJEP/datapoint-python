import unittest
import datapoint

class ManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = datapoint.Manager(api_key="")

    def test_weather_to_text_is_string(self):
        weather_text = self.manager._weather_to_text(0)
        self.assertIsInstance(weather_text, type(""))

    def test_weather_to_text_invalid_input_None(self):
        self.assertRaises(ValueError, self.manager._weather_to_text, None)

    def test_weather_to_text_invalid_input_out_of_bounds(self):
        self.assertRaises(ValueError, self.manager._weather_to_text, 31)

    def test_weather_to_text_invalid_input_String(self):
        self.assertRaises(ValueError, self.manager._weather_to_text, '1')

    def test_visbility_to_text_invalid_input_None(self):
        self.assertRaises(ValueError, self.manager._weather_to_text, None)

    def test_visibility_to_text_invalid_input_out_of_bounds(self):
        self.assertRaises(ValueError, self.manager._weather_to_text, -1)

    def test_visibility_to_text_invalid_input_String(self):
        self.assertRaises(ValueError, self.manager._weather_to_text, '1')
