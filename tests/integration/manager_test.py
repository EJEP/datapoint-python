import datetime
import os
from types import *
from nose.tools import *

import datapoint

class TestManager:

    def __init__(self):
        self.manager = datapoint.Manager(api_key=os.environ['API_KEY'])

    def test_site(self):
        site = self.manager.get_nearest_forecast_site(latitude=51.500728, longitude=-0.124626)
        assert site.name.upper() == 'HORSEGUARDS PARADE'

    def test_get_forecast_sites(self):
        sites = self.manager.get_forecast_sites()
        assert isinstance(sites, list)
        assert sites

    def test_get_daily_forecast(self):
        site = self.manager.get_nearest_forecast_site(latitude=51.500728, longitude=-0.124626)
        forecast = self.manager.get_forecast_for_site(site.id, 'daily')
        assert isinstance(forecast, datapoint.Forecast.Forecast)
        assert forecast.continent.upper() == 'EUROPE'
        assert forecast.country.upper() == 'ENGLAND'
        assert forecast.name.upper() == 'HORSEGUARDS PARADE'
        assert abs(float(forecast.latitude) - 51.500728) < 0.1
        assert abs(float(forecast.longitude) - (-0.124626)) < 0.1
        # Forecast should have been made within last 3 hours
        tz = forecast.data_date.tzinfo
        assert (forecast.data_date
            - datetime.datetime.now(tz=tz) < datetime.timedelta(hours=3))
        # First forecast should be less than 12 hours away
        tz = forecast.days[0].timesteps[0].date.tzinfo
        assert (forecast.days[0].timesteps[0].date -
            datetime.datetime.now(tz=tz) < datetime.timedelta(hours=12))
        for day in forecast.days:
            for timestep in day.timesteps:
                assert timestep.name in ['Day', 'Night']
                assert self.manager._weather_to_text(
                    int(timestep.weather.value)) == timestep.weather.text
                assert -100 < timestep.temperature.value < 100
                assert timestep.temperature.units == 'C'
                assert -100 < timestep.feels_like_temperature.value < 100
                assert timestep.feels_like_temperature.units == 'C'
                assert 0 <= timestep.wind_speed.value < 300
                assert timestep.wind_speed.units == 'mph'
                for char in timestep.wind_direction.value:
                    assert char in ['N', 'E', 'S', 'W']
                assert timestep.wind_direction.units == 'compass'
                assert 0 <= timestep.wind_gust.value < 300
                assert timestep.wind_gust.units == 'mph'
                assert (timestep.visibility.value in
                    ['UN', 'VP', 'PO', 'MO', 'GO', 'VG', 'EX'])
                assert 0 <= timestep.precipitation.value <= 100
                assert timestep.precipitation.units == '%'
                assert 0 <= timestep.humidity.value <= 100
                assert timestep.humidity.units == '%'
                if hasattr(timestep.uv, 'value'):
                    assert 0 < int(timestep.uv.value) < 20

    def test_get_3hour_forecast(self):
        site = self.manager.get_nearest_forecast_site(latitude=51.500728, longitude=-0.124626)
        forecast = self.manager.get_forecast_for_site(site.id, '3hourly')
        assert isinstance(forecast, datapoint.Forecast.Forecast)
        assert forecast.continent.upper() == 'EUROPE'
        assert forecast.country.upper() == 'ENGLAND'
        assert forecast.name.upper() == 'HORSEGUARDS PARADE'
        assert abs(float(forecast.latitude) - 51.500728) < 0.1
        assert abs(float(forecast.longitude) - (-0.124626)) < 0.1
        # Forecast should have been made within last 3 hours
        tz = forecast.data_date.tzinfo
        assert (forecast.data_date
            - datetime.datetime.now(tz=tz) < datetime.timedelta(hours=3))
        # First forecast should be less than 12 hours away
        tz = forecast.days[0].timesteps[0].date.tzinfo
        assert (forecast.days[0].timesteps[0].date -
            datetime.datetime.now(tz=tz) < datetime.timedelta(hours=3))
        for day in forecast.days:
            for timestep in day.timesteps:
                assert isinstance(timestep.name, int)
                assert self.manager._weather_to_text(
                    int(timestep.weather.value)) == timestep.weather.text
                assert -100 < timestep.temperature.value < 100
                assert timestep.temperature.units == 'C'
                assert -100 < timestep.feels_like_temperature.value < 100
                assert timestep.feels_like_temperature.units == 'C'
                assert 0 <= timestep.wind_speed.value < 300
                assert timestep.wind_speed.units == 'mph'
                for char in timestep.wind_direction.value:
                    assert char in ['N', 'E', 'S', 'W']
                assert timestep.wind_direction.units == 'compass'
                assert 0 <= timestep.wind_gust.value < 300
                assert timestep.wind_gust.units == 'mph'
                assert (timestep.visibility.value in
                    ['UN', 'VP', 'PO', 'MO', 'GO', 'VG', 'EX'])
                assert 0 <= timestep.precipitation.value <= 100
                assert timestep.precipitation.units == '%'
                assert 0 <= timestep.humidity.value <= 100
                assert timestep.humidity.units == '%'
                if hasattr(timestep.uv, 'value'):
                    assert 0 <= int(timestep.uv.value) < 20

    def test_get_nearest_observation_site(self):
        site = self.manager.get_nearest_observation_site(longitude=-0.1025, latitude=51.3263)
        assert site.name.upper() == 'KENLEY'

    def test_get_observation_sites(self):
        sites = self.manager.get_observation_sites()
        assert isinstance(sites, list)
        assert sites

    def test_get_observation_with_wind_data(self):
        observation = self.manager.get_observations_for_site(3840)
        assert isinstance(observation, datapoint.Observation.Observation)
        assert observation.continent.upper() == 'EUROPE'
        assert observation.country.upper() == 'ENGLAND'
        assert observation.name.upper() == 'DUNKESWELL AERODROME'

        # Observation should be from within the last hour
        tz = observation.data_date.tzinfo
        assert (observation.data_date
            - datetime.datetime.now(tz=tz) < datetime.timedelta(hours=1))

        # First observation should be between 24 and 25 hours old
        tz = observation.days[0].timesteps[0].date.tzinfo
        assert (datetime.datetime.now(tz=tz) - observation.days[0].timesteps[0].date > datetime.timedelta(hours=24))
        assert (datetime.datetime.now(tz=tz) - observation.days[0].timesteps[0].date < datetime.timedelta(hours=25))

        # Should have total 25 observations across all days
        number_of_timesteps = 0
        for day in observation.days:
            number_of_timesteps += len(day.timesteps)
        assert number_of_timesteps == 25

        for day in observation.days:
            for timestep in day.timesteps:
                assert isinstance(timestep.name, int)
                if timestep.weather.value != 'Not reported':
                    assert self.manager._weather_to_text(int(timestep.weather.value)) == timestep.weather.text
                assert -100 < timestep.temperature.value < 100
                assert timestep.temperature.units == 'C'
                if timestep.wind_speed.value != 'Not reported':
                    assert 0 <= timestep.wind_speed.value < 300
                    assert timestep.wind_speed.units == 'mph'

                if timestep.wind_direction.value != 'Not reported':
                    for char in timestep.wind_direction.value:
                        assert char in ['N', 'E', 'S', 'W']
                        assert timestep.wind_direction.units == 'compass'

                assert 0 <= timestep.visibility.value
                assert (timestep.visibility.text in
                    ['UN', 'VP', 'PO', 'MO', 'GO', 'VG', 'EX'])

                assert 0 <= timestep.humidity.value <= 100
                assert timestep.humidity.units == '%'

                assert -100 < timestep.dew_point.value < 100
                assert timestep.dew_point.units == 'C'

                if timestep.pressure.value != 'Not reported':
                    assert 900 < timestep.pressure.value < 1100
                    assert timestep.pressure.units == 'hpa'

                if timestep.pressure_tendency.value != 'Not reported':
                    assert timestep.pressure_tendency.value in ('R','F','S')
                    assert timestep.pressure_tendency.units == 'Pa/s'


    def test_get_observation_without_wind_data(self):
        observation = self.manager.get_observations_for_site(3220)
        assert isinstance(observation, datapoint.Observation.Observation)
        assert observation.continent.upper() == 'EUROPE'
        assert observation.country.upper() == 'ENGLAND'
        assert observation.name.upper() == 'CARLISLE'

        # Observation should be from within the last hour
        tz = observation.data_date.tzinfo
        assert (observation.data_date
            - datetime.datetime.now(tz=tz) < datetime.timedelta(hours=1))

        # First observation should be between 24 and 25 hours old
        tz = observation.days[0].timesteps[0].date.tzinfo
        assert (datetime.datetime.now(tz=tz) - observation.days[0].timesteps[0].date > datetime.timedelta(hours=24))
        assert (datetime.datetime.now(tz=tz) - observation.days[0].timesteps[0].date < datetime.timedelta(hours=25))

        # Should have total 25 observations across all days
        number_of_timesteps = 0
        for day in observation.days:
            number_of_timesteps += len(day.timesteps)
        assert number_of_timesteps == 25

        for day in observation.days:
            for timestep in day.timesteps:
                assert isinstance(timestep.name, int)
                if timestep.weather.value != 'Not reported':
                    assert self.manager._weather_to_text(
                        int(timestep.weather.value)) == timestep.weather.text
                assert -100 < timestep.temperature.value < 100
                assert timestep.temperature.units == 'C'
                assert timestep.wind_speed is None
                assert timestep.wind_gust is None
                assert timestep.wind_direction is None
                assert 0 <= timestep.visibility.value
                assert (timestep.visibility.text in
                    ['UN', 'VP', 'PO', 'MO', 'GO', 'VG', 'EX'])
                assert 0 <= timestep.humidity.value <= 100
                assert timestep.humidity.units == '%'
                assert -100 < timestep.dew_point.value < 100
                assert timestep.dew_point.units == 'C'
                assert 900 < timestep.pressure.value < 1100
                assert timestep.pressure.units == 'hpa'
                assert timestep.pressure_tendency.value in ('R','F','S')
                assert timestep.pressure_tendency.units == 'Pa/s'
