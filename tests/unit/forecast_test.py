from types import *
from nose.tools import *

import datetime

import datapoint



class TestForecast:

    def __init__(self):
        self.forecast = datapoint.Forecast.Forecast()

    def test_forecast_now_works(self):
        test_day = datapoint.Day.Day()
        test_day.date = datetime.datetime.utcnow()

        test_timestep = datapoint.Timestep.Timestep()
        test_timestep.name = 1

        test_day.timesteps.append(test_timestep)

        self.forecast.days.append(test_day)
        assert self.forecast.now()
