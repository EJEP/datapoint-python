import datetime
import os
from types import *
from nose.tools import *

import datapoint

class TestManager:

    def __init__(self):
        self.manager = datapoint.Manager(api_key=os.environ['API_KEY'])

    def test_site(self):
        site = self.manager.get_nearest_site(-0.124626, 51.500728)
        assert site.name == 'London'

    def test_get_all_sites(self):
        sites = self.manager.get_all_sites()
        assert isinstance(sites, list)
        assert sites

    def test_get_daily_forecast(self):
        site = self.manager.get_nearest_site(-0.124626, 51.500728)
        forecast = self.manager.get_forecast_for_site(site.id, 'daily')
        assert isinstance(forecast, datapoint.Forecast.Forecast)
        assert forecast.continent.upper() == 'EUROPE'
        assert forecast.country.upper() == 'ENGLAND'
        assert forecast.name.upper() == 'LONDON'
        assert abs(float(forecast.longitude) - (-0.124626)) < 0.1
        assert abs(float(forecast.latitude) - 51.500728) < 0.1
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
        site = self.manager.get_nearest_site(-0.124626, 51.500728)
        forecast = self.manager.get_forecast_for_site(site.id, '3hourly')
        assert isinstance(forecast, datapoint.Forecast.Forecast)
        assert forecast.continent.upper() == 'EUROPE'
        assert forecast.country.upper() == 'ENGLAND'
        assert forecast.name.upper() == 'LONDON'
        assert abs(float(forecast.longitude) - (-0.124626)) < 0.1
        assert abs(float(forecast.latitude) - 51.500728) < 0.1
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
        pass
                    
    def test_get_observation_sites(self):
        sites = self.manager.get_observation_sites()
        assert isinstance(sites, list)
        assert sites
        
    def test_get_observation(self):
        pass