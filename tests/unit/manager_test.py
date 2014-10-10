from types import *
from nose.tools import *

import datapoint

class TestManager:

    def __init__(self):
        self.manager = datapoint.Manager(api_key="")

    def test_weather_to_text_is_string(self):
        weather_text = self.manager._weather_to_text(0)
        assert type(weather_text) is StringType

    @raises(ValueError)
    def test_weather_to_text_invalid_input(self):
        weather_text = self.manager._weather_to_text(None)

    @raises(ValueError)
    def test_weather_to_text_out_of_bounds_input(self):
        weather_text = self.manager._weather_to_text(31)
