import pytest
import geojson
from datapoint import Forecast


@pytest.fixture
def hourly_forecast():
    with open('./tests/unit/hourly_api_data.json') as f:
        my_json = geojson.load(f)
    return Forecast.Forecast('hourly', my_json)


class TestForecast:
    def test_hourly_forecast_frequency(self, hourly_forecast):
        assert hourly_forecast.frequency == 'hourly'

    def test_hourly_forecast_location_name(self, hourly_forecast):
        assert hourly_forecast.name == 'Sheffield Park'

    def test_hourly_forecast_location_latitude(self, hourly_forecast):
        assert hourly_forecast.forecast_latitude == 50.9992

    def test_hourly_forecast_location_longitude(self, hourly_forecast):
        assert hourly_forecast.forecast_longitude == 0.0154

    def test_hourly_forecast_distance_from_request(self, hourly_forecast):
        assert hourly_forecast.distance_from_requested_location == 1081.5349
