import datetime

import geojson
import pytest

import tests.reference_data.reference_data_test_forecast as reference_data_test_forecast
from datapoint import Forecast
from datapoint.exceptions import APIException

# TODO look into pytest-cases. Should reduce the amount of stored data structures


@pytest.fixture
def load_hourly_json():
    with open("./tests/reference_data/hourly_api_data.json") as f:
        my_json = geojson.load(f)
    return my_json


@pytest.fixture
def load_daily_json():
    with open("./tests/reference_data/daily_api_data.json") as f:
        my_json = geojson.load(f)
    return my_json


@pytest.fixture
def load_three_hourly_json():
    with open("./tests/reference_data/three_hourly_api_data.json") as f:
        my_json = geojson.load(f)
    return my_json


@pytest.fixture
def daily_forecast(load_daily_json):
    return Forecast.Forecast("daily", load_daily_json, convert_weather_code=True)


@pytest.fixture
def daily_forecast_raw_weather_code(load_daily_json):
    return Forecast.Forecast("daily", load_daily_json, convert_weather_code=False)


@pytest.fixture
def twice_daily_forecast(load_daily_json):
    return Forecast.Forecast("twice-daily", load_daily_json, convert_weather_code=True)


@pytest.fixture
def twice_daily_forecast_raw_weather_code(load_daily_json):
    return Forecast.Forecast("twice-daily", load_daily_json, convert_weather_code=False)


@pytest.fixture
def hourly_forecast(load_hourly_json):
    return Forecast.Forecast("hourly", load_hourly_json, convert_weather_code=True)


@pytest.fixture
def hourly_forecast_raw_weather_code(load_hourly_json):
    return Forecast.Forecast("hourly", load_hourly_json, convert_weather_code=False)


@pytest.fixture
def three_hourly_forecast(load_three_hourly_json):
    return Forecast.Forecast(
        "three-hourly", load_three_hourly_json, convert_weather_code=True
    )


@pytest.fixture
def hourly_first_forecast_and_parameters(load_hourly_json):
    parameters = load_hourly_json["parameters"][0]
    forecast = load_hourly_json["features"][0]["properties"]["timeSeries"][0]
    return (forecast, parameters)


@pytest.fixture
def three_hourly_first_forecast_and_parameters(load_three_hourly_json):
    parameters = load_three_hourly_json["parameters"][0]
    forecast = load_three_hourly_json["features"][0]["properties"]["timeSeries"][0]
    return (forecast, parameters)


@pytest.fixture
def expected_first_hourly_timestep():
    return reference_data_test_forecast.EXPECTED_FIRST_HOURLY_TIMESTEP


@pytest.fixture
def expected_first_hourly_timestep_raw_weather_code():
    return reference_data_test_forecast.EXPECTED_FIRST_HOURLY_TIMESTEP_RAW_WEATHER_CODE


@pytest.fixture
def expected_at_datetime_hourly_timestep():
    return reference_data_test_forecast.EXPECTED_AT_DATETIME_HOURLY_TIMESTEP


@pytest.fixture
def expected_at_datetime_hourly_final_timestep():
    return reference_data_test_forecast.EXPECTED_AT_DATETIME_HOURLY_FINAL_TIMESTEP


@pytest.fixture
def expected_first_daily_timestep():
    return reference_data_test_forecast.EXPECTED_FIRST_DAILY_TIMESTEP


@pytest.fixture
def expected_first_daily_timestep_raw_weather_code():
    return reference_data_test_forecast.EXPECTED_FIRST_DAILY_TIMESTEP_RAW_WEATHER_CODE


@pytest.fixture
def expected_at_datetime_daily_timestep():
    return reference_data_test_forecast.EXPECTED_AT_DATETIME_DAILY_TIMESTEP


@pytest.fixture
def expected_at_datetime_daily_final_timestep():
    return reference_data_test_forecast.EXPECTED_AT_DATETIME_DAILY_FINAL_TIMESTEP


@pytest.fixture
def expected_first_twice_daily_timestep():
    return reference_data_test_forecast.EXPECTED_FIRST_TWICE_DAILY_TIMESTEP


@pytest.fixture
def expected_first_twice_daily_timestep_raw_weather_code():
    return (
        reference_data_test_forecast.EXPECTED_FIRST_TWICE_DAILY_TIMESTEP_RAW_WEATHER_CODE
    )


@pytest.fixture
def expected_at_datetime_twice_daily_timestep():
    return reference_data_test_forecast.EXPECTED_AT_DATETIME_TWICE_DAILY_TIMESTEP


@pytest.fixture
def expected_at_datetime_twice_daily_final_timestep():
    return reference_data_test_forecast.EXPECTED_AT_DATETIME_TWICE_DAILY_FINAL_TIMESTEP


@pytest.fixture
def expected_first_three_hourly_timestep():
    return reference_data_test_forecast.EXPECTED_FIRST_THREE_HOURLY_TIMESTEP


@pytest.fixture
def expected_at_datetime_three_hourly_timestep():
    return reference_data_test_forecast.EXPECTED_AT_DATETIME_THREE_HOURLY_TIMESTEP


@pytest.fixture
def expected_at_datetime_three_hourly_final_timestep():
    return reference_data_test_forecast.EXPECTED_AT_DATETIME_THREE_HOURLY_FINAL_TIMESTEP


class TestHourlyForecast:
    def test_forecast_frequency(self, hourly_forecast):
        assert hourly_forecast.frequency == "hourly"

    def test_forecast_location_name(self, hourly_forecast):
        assert hourly_forecast.name == "Sheffield Park"

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

    def test_build_timestep(
        self,
        hourly_forecast,
        hourly_first_forecast_and_parameters,
        expected_first_hourly_timestep,
    ):
        built_timestep = hourly_forecast._build_timestep(
            hourly_first_forecast_and_parameters[0],
            hourly_first_forecast_and_parameters[1],
        )

        assert built_timestep == expected_first_hourly_timestep

    def test_at_datetime(self, hourly_forecast, expected_at_datetime_hourly_timestep):
        ts = hourly_forecast.at_datetime(datetime.datetime(2024, 2, 16, 19, 15))
        assert ts == expected_at_datetime_hourly_timestep

    def test_at_datetime_final_timestamp(
        self, hourly_forecast, expected_at_datetime_hourly_final_timestep
    ):
        ts = hourly_forecast.at_datetime(datetime.datetime(2024, 2, 17, 19, 20))
        assert ts == expected_at_datetime_hourly_final_timestep

    def test_requested_time_too_early(self, hourly_forecast):
        with pytest.raises(APIException):
            hourly_forecast.at_datetime(datetime.datetime(2024, 2, 15, 18, 25))

    def test_requested_time_too_late(self, hourly_forecast):
        with pytest.raises(APIException):
            hourly_forecast.at_datetime(datetime.datetime(2024, 2, 17, 19, 35))

    def test_forecast_first_timestep_raw_weather_code(
        self,
        hourly_forecast_raw_weather_code,
        expected_first_hourly_timestep_raw_weather_code,
    ):
        assert (
            hourly_forecast_raw_weather_code.timesteps[0]
            == expected_first_hourly_timestep_raw_weather_code
        )


class TestDailyForecast:
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

    # Need a new test_build_timestep function here
    def test_build_timesteps(
        self, daily_forecast, load_daily_json, expected_first_daily_timestep
    ):
        timestep = daily_forecast._build_timestep(
            load_daily_json["features"][0]["properties"]["timeSeries"][0],
            load_daily_json["parameters"][0],
        )
        assert timestep == expected_first_daily_timestep

    def test_at_datetime(self, daily_forecast, expected_at_datetime_daily_timestep):
        ts = daily_forecast.at_datetime(datetime.datetime(2024, 2, 16, 19, 15))
        assert ts == expected_at_datetime_daily_timestep

    def test_at_datetime_final_timestamp(
        self, daily_forecast, expected_at_datetime_daily_final_timestep
    ):
        ts = daily_forecast.at_datetime(datetime.datetime(2024, 2, 17, 17))
        assert ts == expected_at_datetime_daily_final_timestep

    def test_requested_time_too_early(self, daily_forecast):
        with pytest.raises(APIException):
            daily_forecast.at_datetime(datetime.datetime(2024, 2, 15, 17))

    def test_requested_time_too_late(self, daily_forecast):
        with pytest.raises(APIException):
            daily_forecast.at_datetime(datetime.datetime(2024, 2, 23, 19))

    def test_forecast_first_timestep_raw_weather_code(
        self,
        daily_forecast_raw_weather_code,
        expected_first_daily_timestep_raw_weather_code,
    ):
        assert (
            daily_forecast_raw_weather_code.timesteps[0]
            == expected_first_daily_timestep_raw_weather_code
        )


class TestTwiceDailyForecast:
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

    # twice-daily forecasts take daily data from DataHub
    def test_build_twice_daily_timesteps(
        self, twice_daily_forecast, load_daily_json, expected_first_twice_daily_timestep
    ):
        timesteps = twice_daily_forecast._build_twice_daily_timesteps(
            load_daily_json["features"][0]["properties"]["timeSeries"],
            load_daily_json["parameters"][0],
        )
        assert timesteps[0] == expected_first_twice_daily_timestep

    def test_at_datetime(
        self, twice_daily_forecast, expected_at_datetime_twice_daily_timestep
    ):
        ts = twice_daily_forecast.at_datetime(datetime.datetime(2024, 2, 16, 19, 15))
        assert ts == expected_at_datetime_twice_daily_timestep

    def test_at_datetime_final_timestep(
        self, twice_daily_forecast, expected_at_datetime_twice_daily_final_timestep
    ):
        ts = twice_daily_forecast.at_datetime(datetime.datetime(2024, 2, 17, 17))
        assert ts == expected_at_datetime_twice_daily_final_timestep

    def test_requested_time_too_early(self, twice_daily_forecast):
        with pytest.raises(APIException):
            twice_daily_forecast.at_datetime(datetime.datetime(2024, 2, 15, 17))

    def test_requested_time_too_late(self, twice_daily_forecast):
        with pytest.raises(APIException):
            twice_daily_forecast.at_datetime(datetime.datetime(2024, 2, 23, 19))

    def test_forecast_first_timestep_raw_weather_code(
        self,
        twice_daily_forecast_raw_weather_code,
        expected_first_twice_daily_timestep_raw_weather_code,
    ):
        print(twice_daily_forecast_raw_weather_code.timesteps[0])
        assert (
            twice_daily_forecast_raw_weather_code.timesteps[0]
            == expected_first_twice_daily_timestep_raw_weather_code
        )


class TestThreeHourlyForecast:
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

    def test_build_timestep(
        self,
        three_hourly_forecast,
        three_hourly_first_forecast_and_parameters,
        expected_first_three_hourly_timestep,
    ):
        built_timestep = three_hourly_forecast._build_timestep(
            three_hourly_first_forecast_and_parameters[0],
            three_hourly_first_forecast_and_parameters[1],
        )

        assert built_timestep == expected_first_three_hourly_timestep

    def test_at_datetime(
        self, three_hourly_forecast, expected_at_datetime_three_hourly_timestep
    ):
        ts = three_hourly_forecast.at_datetime(datetime.datetime(2024, 2, 22, 19, 15))
        assert ts == expected_at_datetime_three_hourly_timestep

    def test_at_datetime_final_timestamp(
        self, three_hourly_forecast, expected_at_datetime_three_hourly_final_timestep
    ):
        ts = three_hourly_forecast.at_datetime(datetime.datetime(2024, 2, 24, 16))
        assert ts == expected_at_datetime_three_hourly_final_timestep

    def test_requested_time_too_early(self, three_hourly_forecast):
        with pytest.raises(APIException):
            three_hourly_forecast.at_datetime(datetime.datetime(2024, 2, 17, 13, 20))

    def test_requested_time_too_late(self, three_hourly_forecast):
        with pytest.raises(APIException):
            three_hourly_forecast.at_datetime(datetime.datetime(2024, 2, 24, 17))
