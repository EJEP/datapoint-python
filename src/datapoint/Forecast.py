import datetime
from datapoint.exceptions import APIException
from datapoint.Timestep import Timestep
from datapoint.weather_codes import WEATHER_CODES


class Forecast:
    def __init__(self, frequency, api_data):
        self.frequency = frequency
        self.data_date = datetime.datetime.fromisoformat(
            api_data["features"][0]["properties"]["modelRunDate"]
        )
        self.name = api_data["features"][0]["properties"]["location"]
        self.forecast_longitude = api_data["features"][0]["geometry"]["coordinates"][0]
        self.forecast_latitude = api_data["features"][0]["geometry"]["coordinates"][1]
        self.distance_from_requested_location = api_data["features"][0]["properties"][
            "requestPointDistance"
        ]
        # N.B. Elevation is in metres above or below the WGS 84 reference
        # ellipsoid as per GeoJSON spec.
        self.elevation = api_data["features"][0]["geometry"]["coordinates"][2]

        # Need different parsing to cope with daily vs. hourly/three-hourly
        # forecasts. Do hourly first

        forecasts = api_data["features"][0]["properties"]["timeSeries"]
        parameters = api_data["parameters"][0]
        if frequency == "daily":
            self.timesteps = self.__build_timesteps_from_daily(forecasts, parameters)
        else:
            self.timesteps = []
            for forecast in forecasts:
                self.timesteps.append(self.__build_timestep(forecast, parameters))

    def __build_timesteps_from_daily(self, forecasts, parameters):
        timesteps = []
        for forecast in forecasts:
            night_step = {"time": datetime.datetime.fromisoformat(forecast["time"])}
            day_step = {
                "time": datetime.datetime.fromisoformat(forecast["time"])
                + datetime.timedelta(hours=12)
            }

            for element, value in forecast.items():
                if element.startswith("midday"):
                    day_step[element.replace("midday", "")] = {
                        "value": value,
                        "description": parameters[element]["description"],
                        "unit_name": parameters[element]["unit"]["label"],
                        "unit_symbol": parameters[element]["unit"]["symbol"]["type"],
                    }
                elif element.startswith("midnight"):
                    night_step[element.replace("midnight", "")] = {
                        "value": value,
                        "description": parameters[element]["description"],
                        "unit_name": parameters[element]["unit"]["label"],
                        "unit_symbol": parameters[element]["unit"]["symbol"]["type"],
                    }
                elif element.startswith("day"):
                    day_step[element.replace("day", "")] = {
                        "value": value,
                        "description": parameters[element]["description"],
                        "unit_name": parameters[element]["unit"]["label"],
                        "unit_symbol": parameters[element]["unit"]["symbol"]["type"],
                    }
                elif element.startswith("night"):
                    night_step[element.replace("night", "")] = {
                        "value": value,
                        "description": parameters[element]["description"],
                        "unit_name": parameters[element]["unit"]["label"],
                        "unit_symbol": parameters[element]["unit"]["symbol"]["type"],
                    }
                elif element == "maxUvIndex":
                    day_step[element] = {
                        "value": value,
                        "description": parameters[element]["description"],
                        "unit_name": parameters[element]["unit"]["label"],
                        "unit_symbol": parameters[element]["unit"]["symbol"]["type"],
                    }

            timesteps.append(night_step)
            timesteps.append(day_step)

        timesteps = sorted(timesteps, key=lambda t: t["time"])
        return timesteps

    def __build_timestep(self, forecast, parameters):
        timestep = {}
        for element, value in forecast.items():
            if element == "time":
                timestep["time"] = datetime.datetime.fromisoformat(forecast["time"])
            elif element == "significantWeatherCode":
                timestep[element] = {
                    "value": WEATHER_CODES[str(value)],
                    "description": parameters[element]["description"],
                    "unit_name": parameters[element]["unit"]["label"],
                    "unit_symbol": parameters[element]["unit"]["symbol"]["type"],
                }
            else:
                timestep[element] = {
                    "value": value,
                    "description": parameters[element]["description"],
                    "unit_name": parameters[element]["unit"]["label"],
                    "unit_symbol": parameters[element]["unit"]["symbol"]["type"],
                }

        return timestep

    def at_datetime(self, target):
        """Return the timestep closest to the target datetime"""

        # Convert target to offset aware datetime
        if target.tzinfo is None:
            target = datetime.datetime.combine(
                target.date(), target.time(), self.timesteps[0]["time"].tzinfo
            )

        # Check that there is a forecast for the requested time.
        # If we have an hourly forecast, check that the requested time is at
        # most 30 minutes before the first datetime we have a forecast for.
        if self.frequency == "hourly" and target < self.timesteps[0][
            "time"
        ] - datetime.timedelta(hours=0, minutes=30):
            err_str = (
                "There is no forecast available for the requested time. "
                + "The requested time is more than 30 minutes before the first available forecast"
            )
            raise APIException(err_str)

        # If we have a three-hourly forecast, check that the requested time is at
        # most 1.5 hours before the first datetime we have a forecast for.
        if self.frequency == "three-hourly" and target < self.timesteps[0][
            "time"
        ] - datetime.timedelta(hours=1, minutes=30):
            err_str = (
                "There is no forecast available for the requested time. "
                + "The requested time is more than 1 hour and 30 minutes before the first available forecast"
            )
            raise APIException(err_str)

        # If we have a daily forecast, check that the requested time is at
        # most 6 hours before the first datetime we have a forecast for.
        if self.frequency == "daily" and target < self.timesteps[0][
            "time"
        ] - datetime.timedelta(hours=6):
            err_str = (
                "There is no forecast available for the requested time. "
                + "The requested time is more than 6 hours before the first available forecast"
            )

            raise APIException(err_str)

        # If we have an hourly forecast, check that the requested time is at
        # most 30 minutes after the final datetime we have a forecast for
        if self.frequency == "hourly" and target > (
            self.timesteps[-1]["time"] + datetime.timedelta(hours=0, minutes=30)
        ):
            err_str = "There is no forecast available for the requested time. The requested time is more than 30 minutes after the first available forecast"

            raise APIException(err_str)

        # If we have a three-hourly forecast, then the target must be within 1.5
        # hours of the last timestep
        if self.frequency == "three-hourly" and target > (
            self.timesteps[-1]["time"] + datetime.timedelta(hours=1, minutes=30)
        ):
            err_str = "There is no forecast available for the requested time. The requested time is more than 1.5 hours after the first available forecast"

            raise APIException(err_str)

        # If we have a daily forecast, then the target must be within 6 hours
        # of the last timestep
        if self.frequency == "daily" and target > (
            self.timesteps[-1]["time"] + datetime.timedelta(hours=6)
        ):
            err_str = "There is no forecast available for the requested time. The requested time is more than 6 hours after the first available forecast"

            raise APIException(err_str)

        # Loop over all timesteps
        # Calculate the first time difference
        prev_td = target - self.timesteps[0]["time"]
        prev_ts = self.timesteps[0]

        for i, timestep in enumerate(self.timesteps, start=1):
            # Calculate the difference between the target time and the
            # timestep.
            td = target - timestep["time"]

            # Find the timestep which is further from the target than the
            # previous one. Return the previous timestep
            if abs(td.total_seconds()) > abs(prev_td.total_seconds()):
                # We are further from the target
                return prev_ts
            if i == len(self.timesteps):
                return timestep

            prev_ts = timestep
            prev_td = td

    def now(self):
        """Function to return the closest timestep to the current time"""

        d = datetime.datetime.now(tz=self.timesteps[0]["time"].tzinfo)
        return self.at_datetime(d)

    def future(self, in_days=0, in_hours=0, in_minutes=0, in_seconds=0):
        """Return the closest timestep to a date in a given amount of time"""

        d = datetime.datetime.now(tz=self.timesteps[0]["time"].tzinfo)
        target = d + datetime.timedelta(
            days=in_days, hours=in_hours, minutes=in_minutes, seconds=in_seconds
        )

        return self.at_datetime(target)
