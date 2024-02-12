import datetime
import os
import unittest

import datapoint


class ManagerIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = datapoint.Manager(api_key=os.environ['API_KEY'])

    def test_site(self):
        site = self.manager.get_nearest_forecast_site(latitude=51.500728, longitude=-0.124626)
        self.assertEqual(site.name.upper(), 'HORSEGUARDS PARADE')

    def test_get_forecast_sites(self):
        sites = self.manager.get_forecast_sites()
        self.assertIsInstance(sites, list)
        # What is this assert testing
        assert sites

    def test_get_daily_forecast(self):
        site = self.manager.get_nearest_forecast_site(latitude=51.500728, longitude=-0.124626)
        forecast = self.manager.get_forecast_for_site(site.location_id, 'daily')
        self.assertIsInstance(forecast, datapoint.Forecast.Forecast)
        self.assertEqual(forecast.continent.upper(), 'EUROPE')
        self.assertEqual(forecast.country.upper(), 'ENGLAND')
        self.assertEqual(forecast.name.upper(),'HORSEGUARDS PARADE')
        self.assertLess(abs(float(forecast.latitude) - 51.500728), 0.1)
        self.assertLess(abs(float(forecast.longitude) - (-0.124626)), 0.1)
        # Forecast should have been made within last 3 hours
        tz = forecast.data_date.tzinfo
        self.assertLess(forecast.data_date - datetime.datetime.now(tz=tz),
                        datetime.timedelta(hours=3))
        # First forecast should be less than 12 hours away
        tz = forecast.days[0].timesteps[0].date.tzinfo
        self.assertLess(forecast.days[0].timesteps[0].date -
                        datetime.datetime.now(tz=tz),
                        datetime.timedelta(hours=12))
        for day in forecast.days:
            for timestep in day.timesteps:
                self.assertIn(timestep.name, ['Day', 'Night'])
                self.assertEqual(self.manager._weather_to_text(int(timestep.weather.value)),
                                 timestep.weather.text)

                self.assertGreater(timestep.temperature.value, -100)
                self.assertLess(timestep.temperature.value, 100)
                self.assertEqual(timestep.temperature.units, 'C')

                self.assertGreater(timestep.feels_like_temperature.value , -100)
                self.assertLess(timestep.feels_like_temperature.value , 100)
                self.assertEqual(timestep.feels_like_temperature.units, 'C')

                self.assertGreaterEqual(timestep.wind_speed.value, 0)
                self.assertLess(timestep.wind_speed.value, 300)
                self.assertEqual(timestep.wind_speed.units,'mph')

                for char in timestep.wind_direction.value:
                    self.assertIn(char, ['N', 'E', 'S', 'W'])
                self.assertEqual(timestep.wind_direction.units, 'compass')

                self.assertGreaterEqual(timestep.wind_gust.value, 0)
                self.assertLess(timestep.wind_gust.value, 300)
                self.assertEqual(timestep.wind_gust.units, 'mph')

                self.assertIn(timestep.visibility.value,
                    ['UN', 'VP', 'PO', 'MO', 'GO', 'VG', 'EX'])

                self.assertGreaterEqual(timestep.precipitation.value, 0)
                self.assertLessEqual(timestep.precipitation.value, 100)
                self.assertEqual(timestep.precipitation.units, '%')

                self.assertGreaterEqual(timestep.humidity.value, 0)
                self.assertLessEqual(timestep.humidity.value, 100)
                self.assertEqual(timestep.humidity.units, '%')

                if hasattr(timestep.uv, 'value'):
                    self.assertGreaterEqual(int(timestep.uv.value), 0)
                    self.assertLess(int(timestep.uv.value), 30)


    def test_get_3hour_forecast(self):
        site = self.manager.get_nearest_forecast_site(latitude=51.500728, longitude=-0.124626)
        forecast = self.manager.get_forecast_for_site(site.location_id, '3hourly')
        self.assertIsInstance(forecast, datapoint.Forecast.Forecast)
        self.assertEqual(forecast.continent.upper(), 'EUROPE')
        self.assertEqual(forecast.country.upper(), 'ENGLAND')
        self.assertEqual(forecast.name.upper(),'HORSEGUARDS PARADE')
        self.assertLess(abs(float(forecast.latitude) - 51.500728), 0.1)
        self.assertLess(abs(float(forecast.longitude) - (-0.124626)), 0.1)
        # Forecast should have been made within last 3 hours
        tz = forecast.data_date.tzinfo
        self.assertLess(forecast.data_date - datetime.datetime.now(tz=tz),
                        datetime.timedelta(hours=3))
        # First forecast should be less than 12 hours away
        tz = forecast.days[0].timesteps[0].date.tzinfo
        self.assertLess(forecast.days[0].timesteps[0].date -
                        datetime.datetime.now(tz=tz),
                        datetime.timedelta(hours=12))
        for day in forecast.days:
            for timestep in day.timesteps:
                self.assertIsInstance(timestep.name, int)
                self.assertEqual(self.manager._weather_to_text(
                    int(timestep.weather.value)), timestep.weather.text)

                self.assertGreater(timestep.temperature.value, -100)
                self.assertLess(timestep.temperature.value, 100)
                self.assertEqual(timestep.temperature.units, 'C')

                self.assertGreater(timestep.feels_like_temperature.value , -100)
                self.assertLess(timestep.feels_like_temperature.value , 100)
                self.assertEqual(timestep.feels_like_temperature.units, 'C')

                self.assertGreaterEqual(timestep.wind_speed.value, 0)
                self.assertLess(timestep.wind_speed.value, 300)
                self.assertEqual(timestep.wind_speed.units,'mph')

                for char in timestep.wind_direction.value:
                    self.assertIn(char, ['N', 'E', 'S', 'W'])
                self.assertEqual(timestep.wind_direction.units, 'compass')

                self.assertGreaterEqual(timestep.wind_gust.value, 0)
                self.assertLess(timestep.wind_gust.value, 300)
                self.assertEqual(timestep.wind_gust.units, 'mph')

                self.assertIn(timestep.visibility.value,
                    ['UN', 'VP', 'PO', 'MO', 'GO', 'VG', 'EX'])

                self.assertGreaterEqual(timestep.precipitation.value, 0)
                self.assertLessEqual(timestep.precipitation.value, 100)
                self.assertEqual(timestep.precipitation.units, '%')

                self.assertGreaterEqual(timestep.humidity.value, 0)
                self.assertLessEqual(timestep.humidity.value, 100)
                self.assertEqual(timestep.humidity.units, '%')

                if hasattr(timestep.uv, 'value'):
                    self.assertGreaterEqual(int(timestep.uv.value), 0)
                    self.assertLess(int(timestep.uv.value), 30)

    def test_get_nearest_observation_site(self):
        site = self.manager.get_nearest_observation_site(longitude=-0.1025, latitude=51.3263)
        self.assertEqual(site.name.upper(), 'KENLEY')

    def test_get_observation_sites(self):
        sites = self.manager.get_observation_sites()
        self.assertIsInstance(sites, list)
        # Mystery assert
        assert sites

    def test_get_observation_with_wind_data(self):
        observation = self.manager.get_observations_for_site(3840)
        self.assertIsInstance(observation, datapoint.Observation.Observation)
        self.assertEqual(observation.continent.upper(), 'EUROPE')
        self.assertEqual(observation.country.upper(), 'ENGLAND')
        self.assertEqual(observation.name.upper(), 'DUNKESWELL AERODROME')

        # Observation should be from within the last hour
        tz = observation.data_date.tzinfo
        self.assertLess(observation.data_date - datetime.datetime.now(tz=tz),
                        datetime.timedelta(hours=1))

        # First observation should be between 24 and 25 hours old
        tz = observation.days[0].timesteps[0].date.tzinfo
        self.assertGreater(datetime.datetime.now(tz=tz) -
                           observation.days[0].timesteps[0].date,
                           datetime.timedelta(hours=24))
        self.assertLess(datetime.datetime.now(tz=tz) -
                        observation.days[0].timesteps[0].date,
                        datetime.timedelta(hours=25))

        # Should have total 25 observations across all days
        number_of_timesteps = 0
        for day in observation.days:
            number_of_timesteps += len(day.timesteps)
        self.assertEqual(number_of_timesteps, 25)

        for day in observation.days:
            for timestep in day.timesteps:
                self.assertIsInstance(timestep.name, int)
                if timestep.weather.value != 'Not reported':
                    self.assertEqual(self.manager._weather_to_text(int(timestep.weather.value)),
                                     timestep.weather.text)
                self.assertGreater(timestep.temperature.value, -100)
                self.assertLess(timestep.temperature.value, 100)
                self.assertEqual(timestep.temperature.units, 'C')

                if timestep.wind_speed.value != 'Not reported':
                    self.assertGreaterEqual(timestep.wind_speed.value, 0)
                    self.assertLess(timestep.wind_speed.value, 300)
                    self.assertEqual(timestep.wind_speed.units,'mph')

                if timestep.wind_direction.value != 'Not reported':
                    for char in timestep.wind_direction.value:
                        self.assertIn(char, ['N', 'E', 'S', 'W'])
                        self.assertEqual(timestep.wind_direction.units, 'compass')

                self.assertGreaterEqual(timestep.visibility.value, 0)
                self.assertIn(timestep.visibility.text,
                    ['UN', 'VP', 'PO', 'MO', 'GO', 'VG', 'EX'])

                self.assertGreaterEqual(timestep.humidity.value, 0)
                self.assertLessEqual(timestep.humidity.value, 100)
                self.assertEqual(timestep.humidity.units, '%')

                self.assertGreaterEqual(timestep.dew_point.value, 0)
                self.assertLessEqual(timestep.dew_point.value, 100)
                self.assertEqual(timestep.dew_point.units, 'C')

                if timestep.pressure.value != 'Not reported':
                    self.assertGreaterEqual(timestep.pressure.value, 900)
                    self.assertLessEqual(timestep.pressure.value, 1100)
                    self.assertEqual(timestep.pressure.units, 'hpa')

                if timestep.pressure_tendency.value != 'Not reported':
                    self.assertIn(timestep.pressure_tendency.value, ['R','F','S'])
                    self.assertEqual(timestep.pressure_tendency.units, 'Pa/s')


    # def test_get_observation_without_wind_data(self):
    #     observation = self.manager.get_observations_for_site(3220)
    #     assert isinstance(observation, datapoint.Observation.Observation)
    #     assert observation.continent.upper() == 'EUROPE'
    #     assert observation.country.upper() == 'ENGLAND'
    #     assert observation.name.upper() == 'CARLISLE'

    #     # Observation should be from within the last hour
    #     tz = observation.data_date.tzinfo
    #     assert (observation.data_date
    #         - datetime.datetime.now(tz=tz) < datetime.timedelta(hours=1))

    #     # First observation should be between 24 and 25 hours old
    #     tz = observation.days[0].timesteps[0].date.tzinfo
    #     assert (datetime.datetime.now(tz=tz) - observation.days[0].timesteps[0].date > datetime.timedelta(hours=24))
    #     assert (datetime.datetime.now(tz=tz) - observation.days[0].timesteps[0].date < datetime.timedelta(hours=25))

    #     # Should have total 25 observations across all days
    #     number_of_timesteps = 0
    #     for day in observation.days:
    #         number_of_timesteps += len(day.timesteps)
    #     assert number_of_timesteps == 25

    #     for day in observation.days:
    #         for timestep in day.timesteps:
    #             assert isinstance(timestep.name, int)
    #             if timestep.weather.value != 'Not reported':
    #                 assert self.manager._weather_to_text(
    #                     int(timestep.weather.value)) == timestep.weather.text
    #             assert -100 < timestep.temperature.value < 100
    #             assert timestep.temperature.units == 'C'
    #             assert timestep.wind_speed is None
    #             assert timestep.wind_gust is None
    #             assert timestep.wind_direction is None
    #             assert 0 <= timestep.visibility.value
    #             assert (timestep.visibility.text in
    #                 ['UN', 'VP', 'PO', 'MO', 'GO', 'VG', 'EX'])
    #             assert 0 <= timestep.humidity.value <= 100
    #             assert timestep.humidity.units == '%'
    #             assert -100 < timestep.dew_point.value < 100
    #             assert timestep.dew_point.units == 'C'
    #             assert 900 < timestep.pressure.value < 1100
    #             assert timestep.pressure.units == 'hpa'
    #             assert timestep.pressure_tendency.value in ('R','F','S')
    #             assert timestep.pressure_tendency.units == 'Pa/s'
