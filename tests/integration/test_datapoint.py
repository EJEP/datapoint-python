from datetime import datetime, date
import json
import pathlib
import requests
from requests_mock import Mocker
import unittest
from unittest.mock import patch

import datapoint

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"


class MockDateTime(datetime):
	"""Replacement for datetime that can be mocked for testing."""
	def __new__(cls, *args, **kwargs):
		return datetime.__new__(datetime, *args, **kwargs)


class TestDataPoint(unittest.TestCase):
    @Mocker()
    def setUp(self, mock_request):
        with open("{}/datapoint.json".format(pathlib.Path(__file__).parent.absolute())) as f:
            mock_json = json.load(f)

        self.all_sites = json.dumps(mock_json['all_sites'])
        self.wavertree_hourly = json.dumps(mock_json['wavertree_hourly'])
        self.wavertree_daily = json.dumps(mock_json['wavertree_daily'])
        self.kingslynn_hourly = json.dumps(mock_json['kingslynn_hourly'])

        self.conn = datapoint.connection(api_key="abcdefgh-acbd-abcd-abcd-abcdefghijkl")

        mock_request.get('/public/data/val/wxfcs/all/json/sitelist/', text=self.all_sites)
        self.wavertree = self.conn.get_nearest_forecast_site(53.38374, -2.90929)
        self.kingslynn = self.conn.get_nearest_forecast_site(52.75556, 0.44231)


    @Mocker()
    @patch('datetime.datetime', MockDateTime)
    def test_wavertree_hourly(self, mock_request):
        from datetime import datetime, timezone
        MockDateTime.now = classmethod(lambda cls, **kwargs: datetime(2020, 4, 25, 12, tzinfo=timezone.utc))
        mock_request.get('/public/data/val/wxfcs/all/json/354107?res=3hourly', text=self.wavertree_hourly)

        forecast = self.conn.get_forecast_for_site(self.wavertree.id, "3hourly")
        now = forecast.now()

        self.assertEqual(self.wavertree.id, '354107')
        self.assertEqual(self.wavertree.name, 'Wavertree')

        self.assertEqual(now.date.strftime(DATETIME_FORMAT), '2020-04-25 12:00:00+0000')
        self.assertEqual(now.weather.value, '1')
        self.assertEqual(now.temperature.value, 17)
        self.assertEqual(now.feels_like_temperature.value, 14)
        self.assertEqual(now.wind_speed.value, 9)
        self.assertEqual(now.wind_direction.value, 'SSE')
        self.assertEqual(now.wind_gust.value, 16)
        self.assertEqual(now.visibility.value, 'GO')
        self.assertEqual(now.uv.value, '5')
        self.assertEqual(now.precipitation.value, 0)
        self.assertEqual(now.humidity.value, 50)

        self.assertEqual(len(forecast.days), 5)
        self.assertEqual(len(forecast.days[0].timesteps), 7)
        self.assertEqual(len(forecast.days[3].timesteps), 8)

        self.assertEqual(forecast.days[3].timesteps[7].date.strftime(DATETIME_FORMAT), '2020-04-28 21:00:00+0000')
        self.assertEqual(forecast.days[3].timesteps[7].weather.value, '7')
        self.assertEqual(forecast.days[3].timesteps[7].temperature.value, 10)
        self.assertEqual(forecast.days[3].timesteps[7].feels_like_temperature.value, 9)
        self.assertEqual(forecast.days[3].timesteps[7].wind_speed.value, 4)
        self.assertEqual(forecast.days[3].timesteps[7].wind_direction.value, 'NNE')
        self.assertEqual(forecast.days[3].timesteps[7].wind_gust.value, 11)
        self.assertEqual(forecast.days[3].timesteps[7].visibility.value, 'VG')
        self.assertEqual(forecast.days[3].timesteps[7].uv.value, '0')
        self.assertEqual(forecast.days[3].timesteps[7].precipitation.value, 9)
        self.assertEqual(forecast.days[3].timesteps[7].humidity.value, 72)


    @Mocker()
    @patch('datetime.datetime', MockDateTime)
    def test_wavertree_daily(self, mock_request):
        from datetime import datetime, timezone
        MockDateTime.now = classmethod(lambda cls, **kwargs: datetime(2020, 4, 25, 12, tzinfo=timezone.utc))
        mock_request.get('/public/data/val/wxfcs/all/json/354107?res=daily', text=self.wavertree_daily)

        forecast = self.conn.get_forecast_for_site(self.wavertree.id, "daily")
        now = forecast.now()

        self.assertEqual(self.wavertree.id, '354107')
        self.assertEqual(self.wavertree.name, 'Wavertree')

        self.assertEqual(now.date.strftime(DATETIME_FORMAT), '2020-04-25 12:00:00+0000')
        self.assertEqual(now.weather.value, '1')
        self.assertEqual(now.temperature.value, 19)
        self.assertEqual(now.feels_like_temperature.value, 18)
        self.assertEqual(now.wind_speed.value, 9)
        self.assertEqual(now.wind_direction.value, 'SSE')
        self.assertEqual(now.wind_gust.value, 16)
        self.assertEqual(now.visibility.value, 'GO')
        self.assertEqual(now.uv.value, '5')
        self.assertEqual(now.precipitation.value, 2)
        self.assertEqual(now.humidity.value, 50)

        self.assertEqual(len(forecast.days), 5)
        self.assertEqual(len(forecast.days[0].timesteps), 2)
        self.assertEqual(len(forecast.days[4].timesteps), 2)

        self.assertEqual(forecast.days[4].timesteps[1].date.strftime(DATETIME_FORMAT), '2020-04-29 12:00:00+0000')
        self.assertEqual(forecast.days[4].timesteps[1].weather.value, '12')
        self.assertEqual(forecast.days[4].timesteps[1].temperature.value, 13)
        self.assertEqual(forecast.days[4].timesteps[1].feels_like_temperature.value, 10)
        self.assertEqual(forecast.days[4].timesteps[1].wind_speed.value, 13)
        self.assertEqual(forecast.days[4].timesteps[1].wind_direction.value, 'SE')
        self.assertEqual(forecast.days[4].timesteps[1].wind_gust.value, 27)
        self.assertEqual(forecast.days[4].timesteps[1].visibility.value, 'GO')
        self.assertEqual(forecast.days[4].timesteps[1].uv.value, '3')
        self.assertEqual(forecast.days[4].timesteps[1].precipitation.value, 59)
        self.assertEqual(forecast.days[4].timesteps[1].humidity.value, 72)

    @Mocker()
    @patch('datetime.datetime', MockDateTime)
    def test_kingslynn_hourly(self, mock_request):
        from datetime import datetime, timezone
        MockDateTime.now = classmethod(lambda cls, **kwargs: datetime(2020, 4, 25, 12, tzinfo=timezone.utc))
        mock_request.get('/public/data/val/wxfcs/all/json/322380?res=3hourly', text=self.kingslynn_hourly)

        forecast = self.conn.get_forecast_for_site(self.kingslynn.id, "3hourly")
        now = forecast.now()

        self.assertEqual(self.kingslynn.id, '322380')
        self.assertEqual(self.kingslynn.name, "King's Lynn")

        self.assertEqual(now.date.strftime(DATETIME_FORMAT), '2020-04-25 12:00:00+0000')
        self.assertEqual(now.weather.value, '1')
        self.assertEqual(now.temperature.value, 14)
        self.assertEqual(now.feels_like_temperature.value, 13)
        self.assertEqual(now.wind_speed.value, 2)
        self.assertEqual(now.wind_direction.value, 'E')
        self.assertEqual(now.wind_gust.value, 7)
        self.assertEqual(now.visibility.value, 'VG')
        self.assertEqual(now.uv.value, '6')
        self.assertEqual(now.precipitation.value, 0)
        self.assertEqual(now.humidity.value, 60)

        self.assertEqual(len(forecast.days), 5)
        self.assertEqual(len(forecast.days[0].timesteps), 7)
        self.assertEqual(len(forecast.days[4].timesteps), 8)

        self.assertEqual(forecast.days[4].timesteps[5].date.strftime(DATETIME_FORMAT), '2020-04-29 15:00:00+0000')
        self.assertEqual(forecast.days[4].timesteps[5].weather.value, '12')
        self.assertEqual(forecast.days[4].timesteps[5].temperature.value, 14)
        self.assertEqual(forecast.days[4].timesteps[5].feels_like_temperature.value, 12)
        self.assertEqual(forecast.days[4].timesteps[5].wind_speed.value, 13)
        self.assertEqual(forecast.days[4].timesteps[5].wind_direction.value, 'S')
        self.assertEqual(forecast.days[4].timesteps[5].wind_gust.value, 27)
        self.assertEqual(forecast.days[4].timesteps[5].visibility.value, 'GO')
        self.assertEqual(forecast.days[4].timesteps[5].uv.value, '1')
        self.assertEqual(forecast.days[4].timesteps[5].precipitation.value, 55)
        self.assertEqual(forecast.days[4].timesteps[5].humidity.value, 68)

if __name__ == '__main__':
    unittest.main()
