from types import *
from nose.tools import *

import datetime

import datapoint


class TestForecast:

    def __init__(self):
        self.forecast = datapoint.Forecast.Forecast()

    def test_forecast_now_works(self):
        test_day_0 = datapoint.Day.Day()
        test_day_0.date = datetime.datetime.now(datetime.timezone.utc)

        test_timestep_0 = datapoint.Timestep.Timestep()
        test_timestep_0.name = 0
        test_timestep_0.date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=2)

        test_timestep_1 = datapoint.Timestep.Timestep()
        test_timestep_1.name = 1
        test_timestep_1.date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=4)

        test_day_0.timesteps.append(test_timestep_0)
        test_day_0.timesteps.append(test_timestep_1)

        self.forecast.days.append(test_day_0)

        test_day_1 = datapoint.Day.Day()
        for i in range(8):
            ts = datapoint.Timestep.Timestep()
            ts.name = i * 180
            ts.date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1, hours=i*3)

            test_day_1.timesteps.append(ts)
        self.forecast.days.append(test_day_1)

        assert self.forecast.now()
