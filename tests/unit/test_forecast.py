import datetime
import datapoint
import unittest


class TestForecast(unittest.TestCase):

    def setUp(self):
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

        # What is being asserted here?
        #print(self.forecast.now())
        assert self.forecast.now()

    def test_at_datetime_1_5_hours_before_after(self):

        # Generate 8 timesteps These are set at 00:00, 03:00, 06:00, 09:00,
        # 12:00, 15:00, 18:00, 21:00 and don't got far into the past For this
        # test we are checking the forecast for 07:00 on 2020-03-03, at 08:45
        # on 2020-03-03 so we need timesteps from 09:00 (5 of them) and the day
        # after Also checked is the forecast for 23:00 on 2020-03-04. These
        # both raise APIException

        test_day_0 = datapoint.Day.Day()
        test_day_0.date = datetime.datetime(2020, 3, 3, tzinfo=datetime.timezone.utc)

        for i in range(5):
            ts = datapoint.Timestep.Timestep()
            ts.name = 9+(3*i)
            ts.date = datetime.datetime(2020, 3, 3, 9+(3*i), tzinfo=datetime.timezone.utc)
            test_day_0.timesteps.append(ts)

        test_day_1 = datapoint.Day.Day()
        test_day_1.date = datetime.datetime(2020, 3, 4, tzinfo=datetime.timezone.utc)

        for i in range(8):
            ts = datapoint.Timestep.Timestep()
            ts.name = 3*i
            ts.date = datetime.datetime(2020, 3, 4, 3*i, tzinfo=datetime.timezone.utc)
            test_day_1.timesteps.append(ts)

        forecast = datapoint.Forecast.Forecast()

        forecast.days.append(test_day_0)
        forecast.days.append(test_day_1)

        target_before = datetime.datetime(2020, 3, 3, 7, 0,
                                          tzinfo=datetime.timezone.utc)

        target_after = datetime.datetime(2020, 3, 4, 23, 0,
                                          tzinfo=datetime.timezone.utc)


        self.assertRaises(datapoint.exceptions.APIException,
                          forecast.at_datetime, target_before)

        self.assertRaises(datapoint.exceptions.APIException,
                          forecast.at_datetime, target_after)

    def test_at_datetime_6_hours_before_after(self):

        # Generate 2 timesteps These are set at 00:00 and 12:00

        test_day_0 = datapoint.Day.Day()
        test_day_0.date = datetime.datetime(2020, 3, 3, tzinfo=datetime.timezone.utc)

        for i in range(2):
            ts = datapoint.Timestep.Timestep()
            ts.name = 2*i
            ts.date = datetime.datetime(2020, 3, 3, 2*i, tzinfo=datetime.timezone.utc)
            test_day_0.timesteps.append(ts)

        test_day_1 = datapoint.Day.Day()
        test_day_1.date = datetime.datetime(2020, 3, 4, tzinfo=datetime.timezone.utc)

        for i in range(2):
            ts = datapoint.Timestep.Timestep()
            ts.name = 2*i
            ts.date = datetime.datetime(2020, 3, 4, 2*i, tzinfo=datetime.timezone.utc)
            test_day_1.timesteps.append(ts)

        forecast = datapoint.Forecast.Forecast()

        forecast.days.append(test_day_0)
        forecast.days.append(test_day_1)

        target_before = datetime.datetime(2020, 3, 2, 15, 0,
                                          tzinfo=datetime.timezone.utc)

        target_after = datetime.datetime(2020, 3, 6, 7, 0,
                                          tzinfo=datetime.timezone.utc)


        self.assertRaises(datapoint.exceptions.APIException,
                          forecast.at_datetime, target_before)

        self.assertRaises(datapoint.exceptions.APIException,
                          forecast.at_datetime, target_after)
