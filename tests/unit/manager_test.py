from types import *
from nose.tools import *

import datapoint

class TestManager:

    def __init__(self):
        self.manager = datapoint.Manager(api_key="")

    def test_weather_to_text_is_string(self):
        weather_text = self.manager._weather_to_text(0)
        assert isinstance(weather_text, type(""))

    @raises(ValueError)
    def test_weather_to_text_invalid_input_None(self):
        weather_text = self.manager._weather_to_text(None)

    @raises(ValueError)
    def test_weather_to_text_invalid_input_out_of_bounds(self):
        weather_text = self.manager._weather_to_text(31)

    @raises(ValueError)
    def test_weather_to_text_invalid_input_String(self):
        weather_text = self.manager._weather_to_text('1')
        
    @raises(ValueError)
    def test_visbility_to_text_invalid_input_None(self):
        visibility = self.manager._weather_to_text(None)

    @raises(ValueError)
    def test_visibility_to_text_invalid_input_out_of_bounds(self):
        visibility = self.manager._weather_to_text(-1)

    @raises(ValueError)
    def test_visibility_to_text_invalid_input_String(self):
        visibility = self.manager._weather_to_text('1')