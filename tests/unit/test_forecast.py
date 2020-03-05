import datetime
import datapoint
import unittest


class TestForecast(unittest.TestCase):

    def setUp(self):
        self.forecast_3hrly = datapoint.Forecast.Forecast()

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

        self.forecast_3hrly.days.append(test_day_0)
        self.forecast_3hrly.days.append(test_day_1)

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

        self.forecast_daily = datapoint.Forecast.Forecast()

        self.forecast_daily.days.append(test_day_0)
        self.forecast_daily.days.append(test_day_1)


    def test_forecast_now_works(self):
        forecast = datapoint.Forecast.Forecast()
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

        forecast.days.append(test_day_0)

        test_day_1 = datapoint.Day.Day()
        for i in range(8):
            ts = datapoint.Timestep.Timestep()
            ts.name = i * 180
            ts.date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1, hours=i*3)

            test_day_1.timesteps.append(ts)
        forecast.days.append(test_day_1)

        # What is being asserted here?
        #print(self.forecast.now())
        assert forecast.now()

    def test_at_datetime_1_5_hours_before_after(self):

        target_before = datetime.datetime(2020, 3, 3, 7, 0,
                                          tzinfo=datetime.timezone.utc)

        target_after = datetime.datetime(2020, 3, 4, 23, 0,
                                          tzinfo=datetime.timezone.utc)

        self.assertRaises(datapoint.exceptions.APIException,
                          self.forecast_3hrly.at_datetime, target_before)

        self.assertRaises(datapoint.exceptions.APIException,
                          self.forecast_3hrly.at_datetime, target_after)

    def test_at_datetime_6_hours_before_after(self):

        # Generate 2 timesteps These are set at 00:00 and 12:00

        target_before = datetime.datetime(2020, 3, 2, 15, 0,
                                          tzinfo=datetime.timezone.utc)

        target_after = datetime.datetime(2020, 3, 6, 7, 0,
                                          tzinfo=datetime.timezone.utc)

        self.assertRaises(datapoint.exceptions.APIException,
                          self.forecast_daily.at_datetime, target_before)

        self.assertRaises(datapoint.exceptions.APIException,
                          self.forecast_daily.at_datetime, target_after)

    def test_normal_time(self):
        target = datetime.datetime(2020, 3, 3, 10, 0,
                                          tzinfo=datetime.timezone.utc)

        nearest = self.forecast_3hrly.at_datetime(target)
        expected = datetime.datetime(2020, 3, 3, 9,
                                     tzinfo=datetime.timezone.utc)
        self.assertEqual(nearest.date, expected)

        target = datetime.datetime(2020, 3, 3, 11, 0,
                                          tzinfo=datetime.timezone.utc)

        nearest = self.forecast_3hrly.at_datetime(target)
        expected = datetime.datetime(2020, 3, 3, 12,
                                     tzinfo=datetime.timezone.utc)
        self.assertEqual(nearest.date, expected)


    def test_forecase_midnight(self):
        target = datetime.datetime(2020, 3, 4, 0, 15,
                                          tzinfo=datetime.timezone.utc)

        nearest = self.forecast_3hrly.at_datetime(target)
        expected = datetime.datetime(2020, 3, 4, 0,
                                     tzinfo=datetime.timezone.utc)
        self.assertEqual(nearest.date, expected)


