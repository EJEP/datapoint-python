import pytest
import requests

import tests.reference_data.reference_data_test_forecast as reference_data_test_forecast
from datapoint.Manager import Manager


class MockResponseHourly:
    def __init__(self):
        with open("./tests/reference_data/hourly_api_data.json") as f:
            my_json = f.read()

        self.text = my_json

    @staticmethod
    def raise_for_status():
        pass


@pytest.fixture
def _mock_response_hourly(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseHourly()

    monkeypatch.setattr(requests.Session, "get", mock_get)


@pytest.fixture
def hourly_forecast(_mock_response_hourly):
    m = Manager(api_key="aaaaaaaaaaaaaaaaaaaaaaaaa")
    f = m.get_forecast(50.9992, 0.0154, frequency="hourly", convert_weather_code=True)
    return f


@pytest.fixture
def expected_first_hourly_timestep():
    return reference_data_test_forecast.EXPECTED_FIRST_HOURLY_TIMESTEP


class MockResponseThreeHourly:
    def __init__(self):
        with open("./tests/reference_data/three_hourly_api_data.json") as f:
            my_json = f.read()

        self.text = my_json

    @staticmethod
    def raise_for_status():
        pass


@pytest.fixture
def _mock_response_three_hourly(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseThreeHourly()

    monkeypatch.setattr(requests.Session, "get", mock_get)


@pytest.fixture
def three_hourly_forecast(_mock_response_three_hourly):
    m = Manager(api_key="aaaaaaaaaaaaaaaaaaaaaaaaa")
    f = m.get_forecast(
        50.9992, 0.0154, frequency="three-hourly", convert_weather_code=True
    )
    return f


@pytest.fixture
def expected_first_three_hourly_timestep():
    return reference_data_test_forecast.EXPECTED_FIRST_THREE_HOURLY_TIMESTEP


class MockResponseDaily:
    def __init__(self):
        with open("./tests/reference_data/daily_api_data.json") as f:
            my_json = f.read()

        self.text = my_json

    @staticmethod
    def raise_for_status():
        pass


@pytest.fixture
def _mock_response_daily(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseDaily()

    monkeypatch.setattr(requests.Session, "get", mock_get)


@pytest.fixture
def daily_forecast(_mock_response_daily):
    m = Manager(api_key="aaaaaaaaaaaaaaaaaaaaaaaaa")
    f = m.get_forecast(50.9992, 0.0154, frequency="daily", convert_weather_code=True)
    return f


@pytest.fixture
def twice_daily_forecast(_mock_response_daily):
    m = Manager(api_key="aaaaaaaaaaaaaaaaaaaaaaaaa")
    f = m.get_forecast(
        50.9992, 0.0154, frequency="twice-daily", convert_weather_code=True
    )
    return f


@pytest.fixture
def expected_first_daily_timestep():
    return reference_data_test_forecast.EXPECTED_FIRST_DAILY_TIMESTEP


@pytest.fixture
def expected_first_twice_daily_timestep():
    return reference_data_test_forecast.EXPECTED_FIRST_TWICE_DAILY_TIMESTEP


class TestHourly:
    def test_location_name(self, hourly_forecast):
        assert hourly_forecast.name == "Sheffield Park"

    def test_forecast_frequency(self, hourly_forecast):
        assert hourly_forecast.frequency == "hourly"

    def test_forecast_location_latitude(self, hourly_forecast):
        assert hourly_forecast.forecast_latitude == 50.9992

    def test_forecast_location_longitude(self, hourly_forecast):
        assert hourly_forecast.forecast_longitude == 0.0154

    def test_forecast_distance_from_request(self, hourly_forecast):
        assert hourly_forecast.distance_from_requested_location == 1081.5349

    def test_forecast_elevation(self, hourly_forecast):
        assert hourly_forecast.elevation == 37.0

    def test_forecast_first_timestep(
        self, hourly_forecast, expected_first_hourly_timestep
    ):
        assert hourly_forecast.timesteps[0] == expected_first_hourly_timestep


class TestThreeHourly:
    def test_forecast_frequency(self, three_hourly_forecast):
        assert three_hourly_forecast.frequency == "three-hourly"

    def test_forecast_location_name(self, three_hourly_forecast):
        assert three_hourly_forecast.name == "Sheffield Park"

    def test_forecast_location_latitude(self, three_hourly_forecast):
        assert three_hourly_forecast.forecast_latitude == 50.9992

    def test_forecast_location_longitude(self, three_hourly_forecast):
        assert three_hourly_forecast.forecast_longitude == 0.0154

    def test_forecast_distance_from_request(self, three_hourly_forecast):
        assert three_hourly_forecast.distance_from_requested_location == 1081.5349

    def test_forecast_elevation(self, three_hourly_forecast):
        assert three_hourly_forecast.elevation == 37.0

    def test_forecast_first_timestep(
        self, three_hourly_forecast, expected_first_three_hourly_timestep
    ):
        assert (
            three_hourly_forecast.timesteps[0] == expected_first_three_hourly_timestep
        )


class TestDaily:
    def test_forecast_frequency(self, daily_forecast):
        assert daily_forecast.frequency == "daily"

    def test_forecast_location_name(self, daily_forecast):
        assert daily_forecast.name == "Sheffield Park"

    def test_forecast_location_latitude(self, daily_forecast):
        assert daily_forecast.forecast_latitude == 50.9992

    def test_forecast_location_longitude(self, daily_forecast):
        assert daily_forecast.forecast_longitude == 0.0154

    def test_forecast_distance_from_request(self, daily_forecast):
        assert daily_forecast.distance_from_requested_location == 1081.5349

    def test_forecast_elevation(self, daily_forecast):
        assert daily_forecast.elevation == 37.0

    def test_forecast_first_timestep(
        self, daily_forecast, expected_first_daily_timestep
    ):
        assert daily_forecast.timesteps[0] == expected_first_daily_timestep


class TestTwiceDaily:
    def test_forecast_frequency(self, twice_daily_forecast):
        assert twice_daily_forecast.frequency == "twice-daily"

    def test_forecast_location_name(self, twice_daily_forecast):
        assert twice_daily_forecast.name == "Sheffield Park"

    def test_forecast_location_latitude(self, twice_daily_forecast):
        assert twice_daily_forecast.forecast_latitude == 50.9992

    def test_forecast_location_longitude(self, twice_daily_forecast):
        assert twice_daily_forecast.forecast_longitude == 0.0154

    def test_forecast_distance_from_request(self, twice_daily_forecast):
        assert twice_daily_forecast.distance_from_requested_location == 1081.5349

    def test_forecast_elevation(self, twice_daily_forecast):
        assert twice_daily_forecast.elevation == 37.0

    def test_forecast_first_timestep(
        self, twice_daily_forecast, expected_first_twice_daily_timestep
    ):
        assert twice_daily_forecast.timesteps[0] == expected_first_twice_daily_timestep
