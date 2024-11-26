import datetime

from datapoint.exceptions import APIException
from datapoint.weather_codes import WEATHER_CODES


class Forecast:
    """Forecast data returned from DataHub

    Provides access to forecasts as far ahead as provided by DataHub. See the
    DataHub documentation for the latest limits on the forecast range. The
    values of data from DataHub are combined with the unit information and
    description and returned as a dict.

    Basic Usage::

      >>> import datapoint
      >>> m = datapoint.Manager.Manager(api_key = "blah")
      >>> f = m.get_forecast(
                  latitude=50,
                  longitude=0,
                  frequency="hourly",
                  convert_weather_code=True,
              )
      >>> f.now()
      {
          'time': datetime.datetime(2024, 2, 19, 13, 0, tzinfo=datetime.timezone.utc),
          'screenTemperature': {
              'value': 10.09,
              'description': 'Screen Air Temperature',
              'unit_name': 'degrees Celsius',
              'unit_symbol': 'Cel'
          },
          'screenDewPointTemperature': {
              'value': 8.08,
              'description': 'Screen Dew Point Temperature',
              'unit_name': 'degrees Celsius',
              'unit_symbol': 'Cel'
          },
          'feelsLikeTemperature': {
              'value': 6.85,
              'description': 'Feels Like Temperature',
              'unit_name': 'degrees Celsius',
              'unit_symbol': 'Cel'
          },
          'windSpeed10m': {
              'value': 7.57,
              'description': '10m Wind Speed',
              'unit_name': 'metres per second',
              'unit_symbol': 'm/s'
          },
          'windDirectionFrom10m': {
              'value': 263,
              'description': '10m Wind From Direction',
              'unit_name': 'degrees',
              'unit_symbol': 'deg'
          },
          'windGustSpeed10m': {
              'value': 12.31,
              'description': '10m Wind Gust Speed',
              'unit_name': 'metres per second',
              'unit_symbol': 'm/s'
          },
          'visibility': {
              'value': 21201,
              'description': 'Visibility',
              'unit_name': 'metres',
              'unit_symbol': 'm'
          },
          'screenRelativeHumidity': {
              'value': 87.81,
              'description': 'Screen Relative Humidity',
              'unit_name': 'percentage',
              'unit_symbol': '%'
          },
          'mslp': {
              'value': 103080,
              'description': 'Mean Sea Level Pressure',
              'unit_name': 'pascals',
              'unit_symbol': 'Pa'
          },
          'uvIndex': {
              'value': 1,
              'description': 'UV Index',
              'unit_name': 'dimensionless',
              'unit_symbol': '1'
          },
          'significantWeatherCode': {
              'value': 'Cloudy',
              'description': 'Significant Weather Code',
              'unit_name': 'dimensionless',
              'unit_symbol': '1'
          },
          'precipitationRate': {
              'value': 0.0,
              'description': 'Precipitation Rate',
              'unit_name': 'millimetres per hour',
              'unit_symbol': 'mm/h'
          },
          'probOfPrecipitation': {
              'value': 21,
              'description': 'Probability of Precipitation',
              'unit_name': 'percentage',
              'unit_symbol': '%'
          }
      }
    """

    def __init__(self, frequency, api_data, convert_weather_code):
        """
        :param frequency: Frequency of forecast: 'hourly', 'three-hourly' or 'daily'
        :param api_data: Data returned from API call
        :param: convert_weather_code: Convert numeric weather codes to string description
        :type frequency: string
        :type api_data: dict
        :type convert_weather_code: bool
        """
        self.frequency = frequency
        # Need to parse format like 2024-02-17T15:00Z. This can only be
        # done with datetime.datetime.fromisoformat from python 3.11
        # onwards.
        self.data_date = datetime.datetime.strptime(
            api_data["features"][0]["properties"]["modelRunDate"],
            "%Y-%m-%dT%H:%M%z",
        )  #: The date the provided forecast was generated.

        self.forecast_longitude = api_data["features"][0]["geometry"]["coordinates"][
            0
        ]  #: The longitude of the provided forecast.
        self.forecast_latitude = api_data["features"][0]["geometry"]["coordinates"][
            1
        ]  #: The latitude of the provided forecast.
        self.distance_from_requested_location = api_data["features"][0]["properties"][
            "requestPointDistance"
        ]  #: The distance of the location of the provided forecast from the requested location
        self.name = api_data["features"][0]["properties"]["location"][
            "name"
        ]  #: The name of the location of the provided forecast

        # N.B. Elevation is in metres above or below the WGS 84 reference
        # ellipsoid as per GeoJSON spec.
        self.elevation = api_data["features"][0]["geometry"]["coordinates"][
            2
        ]  #: The elevation of the location of the provided forecast

        self.convert_weather_code = (
            convert_weather_code  #: Convert numeric weather codes to string description
        )

        forecasts = api_data["features"][0]["properties"]["timeSeries"]
        parameters = api_data["parameters"][0]
        if frequency == "daily":
            self.timesteps = self._build_timesteps_from_daily(forecasts, parameters)
        else:
            self.timesteps = []
            for forecast in forecasts:
                self.timesteps.append(self._build_timestep(forecast, parameters))

    def _build_timesteps_from_daily(self, forecasts, parameters):
        """Build individual timesteps from forecasts and metadata

        Take the forecast data from DataHub and combine with unit information
        in each timestep. Break each day into day and night steps. ASSUME that
        each step has data for the night referred to in the timestamp and the
        following dawn-dusk period.

        :parameter forecasts: Forecast data from DataHub
        :parameter parameters: Unit information from DataHub
        :type forecasts: list
        :type parameters: dict

        :return: List of timesteps
        :rtype: list
        """

        timesteps = []
        for forecast in forecasts:
            # Need to parse format like 2024-02-17T15:00Z. This can only be
            # done with datetime.datetime.fromisoformat from python 3.11
            # onwards.
            night_step = {
                "time": datetime.datetime.strptime(forecast["time"], "%Y-%m-%dT%H:%M%z")
            }
            day_step = {
                "time": datetime.datetime.strptime(forecast["time"], "%Y-%m-%dT%H:%M%z")
                + datetime.timedelta(hours=12)
            }

            for element, value in forecast.items():
                if element.startswith("midday"):
                    trimmed_element = element.replace("midday", "")
                    case_corrected_element = (
                        trimmed_element[0].lower() + trimmed_element[1:]
                    )
                    day_step[case_corrected_element] = {
                        "value": value,
                        "description": parameters[element]["description"],
                        "unit_name": parameters[element]["unit"]["label"],
                        "unit_symbol": parameters[element]["unit"]["symbol"]["type"],
                    }
                elif element.startswith("midnight"):
                    trimmed_element = element.replace("midnight", "")
                    case_corrected_element = (
                        trimmed_element[0].lower() + trimmed_element[1:]
                    )
                    night_step[case_corrected_element] = {
                        "value": value,
                        "description": parameters[element]["description"],
                        "unit_name": parameters[element]["unit"]["label"],
                        "unit_symbol": parameters[element]["unit"]["symbol"]["type"],
                    }
                elif element.startswith("day"):
                    trimmed_element = element.replace("day", "")
                    case_corrected_element = (
                        trimmed_element[0].lower() + trimmed_element[1:]
                    )

                    if (
                        case_corrected_element == "significantWeatherCode"
                        and self.convert_weather_code
                    ):
                        day_step[case_corrected_element] = {
                            "value": WEATHER_CODES[str(value)],
                            "description": parameters[element]["description"],
                            "unit_name": parameters[element]["unit"]["label"],
                            "unit_symbol": parameters[element]["unit"]["symbol"][
                                "type"
                            ],
                        }

                    else:
                        day_step[case_corrected_element] = {
                            "value": value,
                            "description": parameters[element]["description"],
                            "unit_name": parameters[element]["unit"]["label"],
                            "unit_symbol": parameters[element]["unit"]["symbol"][
                                "type"
                            ],
                        }
                elif element.startswith("night"):
                    trimmed_element = element.replace("night", "")
                    case_corrected_element = (
                        trimmed_element[0].lower() + trimmed_element[1:]
                    )

                    if (
                        case_corrected_element == "significantWeatherCode"
                        and self.convert_weather_code
                    ):
                        night_step[case_corrected_element] = {
                            "value": WEATHER_CODES[str(value)],
                            "description": parameters[element]["description"],
                            "unit_name": parameters[element]["unit"]["label"],
                            "unit_symbol": parameters[element]["unit"]["symbol"][
                                "type"
                            ],
                        }

                    else:
                        night_step[case_corrected_element] = {
                            "value": value,
                            "description": parameters[element]["description"],
                            "unit_name": parameters[element]["unit"]["label"],
                            "unit_symbol": parameters[element]["unit"]["symbol"][
                                "type"
                            ],
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

    def _build_timestep(self, forecast, parameters):
        """Build individual timestep from forecast and metadata

        Take the forecast data from DataHub for a single time and combine with
        unit information in each timestep.

        :parameter forecast: Forecast data from DataHub
        :parameter parameters: Unit information from DataHub
        :type forecast: dict
        :type parameters:dict

        :return: Individual forecast timestep
        :rtype: dict

        """

        timestep = {}
        for element, value in forecast.items():
            if element == "time":
                # Need to parse format like 2024-02-17T15:00Z. This can only be
                # done with datetime.datetime.fromisoformat from python 3.11
                # onwards.
                timestep["time"] = datetime.datetime.strptime(
                    forecast["time"], "%Y-%m-%dT%H:%M%z"
                )

            elif element == "significantWeatherCode" and self.convert_weather_code:
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

    def _check_requested_time(self, target):
        """Check that a forecast for the requested time can be provided

        :parameter target: The requested time for the forecast
        :type target: datetime
        """
        # Check that there is a forecast for the requested time.
        # If we have an hourly forecast, check that the requested time is at
        # most 30 minutes before the first datetime we have a forecast for.
        if self.frequency == "hourly" and target < self.timesteps[0][
            "time"
        ] - datetime.timedelta(hours=0, minutes=30):
            err_str = (
                "There is no forecast available for the requested time. "
                "The requested time is more than 30 minutes before the "
                "first available forecast."
            )
            raise APIException(err_str)

        # If we have a three-hourly forecast, check that the requested time is at
        # most 1.5 hours before the first datetime we have a forecast for.
        if self.frequency == "three-hourly" and target < self.timesteps[0][
            "time"
        ] - datetime.timedelta(hours=1, minutes=30):
            err_str = (
                "There is no forecast available for the requested time. "
                "The requested time is more than 1 hour and 30 minutes "
                "before the first available forecast."
            )
            raise APIException(err_str)

        # If we have a daily forecast, check that the requested time is at
        # most 6 hours before the first datetime we have a forecast for.
        if self.frequency == "daily" and target < self.timesteps[0][
            "time"
        ] - datetime.timedelta(hours=6):
            err_str = (
                "There is no forecast available for the requested time. "
                "The requested time is more than 6 hours before the first "
                "available forecast."
            )

            raise APIException(err_str)

        # If we have an hourly forecast, check that the requested time is at
        # most 30 minutes after the final datetime we have a forecast for
        if self.frequency == "hourly" and target > (
            self.timesteps[-1]["time"] + datetime.timedelta(hours=0, minutes=30)
        ):
            err_str = (
                "There is no forecast available for the requested time. The "
                "requested time is more than 30 minutes after the first "
                "available forecast"
            )

            raise APIException(err_str)

        # If we have a three-hourly forecast, then the target must be within 1.5
        # hours of the last timestep
        if self.frequency == "three-hourly" and target > (
            self.timesteps[-1]["time"] + datetime.timedelta(hours=1, minutes=30)
        ):
            err_str = (
                "There is no forecast available for the requested time. The "
                "requested time is more than 1.5 hours after the first "
                "available forecast."
            )

            raise APIException(err_str)

        # If we have a daily forecast, then the target must be within 6 hours
        # of the last timestep
        if self.frequency == "daily" and target > (
            self.timesteps[-1]["time"] + datetime.timedelta(hours=6)
        ):
            err_str = (
                "There is no forecast available for the requested time. The "
                "requested time is more than 6 hours after the first available "
                "forecast."
            )

            raise APIException(err_str)

    def at_datetime(self, target):
        """Return the timestep closest to the target datetime

        :parameter target: Time to get the forecast for
        :type target: datetime

        :return: Individual forecast timestep
        :rtype: dict

        """

        # Convert target to offset aware datetime
        if target.tzinfo is None:
            target = datetime.datetime.combine(
                target.date(), target.time(), self.timesteps[0]["time"].tzinfo
            )

        self._check_requested_time(target)

        # Loop over all timesteps
        # Calculate the first time difference
        prev_td = target - self.timesteps[0]["time"]
        prev_ts = self.timesteps[0]
        to_return = None

        for i, timestep in enumerate(self.timesteps, start=1):
            # Calculate the difference between the target time and the
            # timestep.
            td = target - timestep["time"]

            # Find the timestep which is further from the target than the
            # previous one. Return the previous timestep
            if abs(td.total_seconds()) > abs(prev_td.total_seconds()):
                # We are further from the target
                to_return = prev_ts
                break
            if i == len(self.timesteps):
                to_return = timestep

            prev_ts = timestep
            prev_td = td
        return to_return

    def now(self):
        """Return the closest timestep to the current time

        :return: Individual forecast timestep
        :rtype: dict
        """

        d = datetime.datetime.now(tz=self.timesteps[0]["time"].tzinfo)
        return self.at_datetime(d)

    def future(self, days=0, hours=0, minutes=0):
        """Return the closest timestep to a date in a given amount of time

        Either provide components of the time to the forecast or the total
        hours or minutes

        Providing components::

        >>> import datapoint
        >>> m = datapoint.Manager(api_key = "blah")
        >>> f = m.get_forecast(latitude=50, longitude=0, frequency="hourly")
        >>> f.future(days=1, hours=2)

        Providing total hours::

        >>> import datapoint
        >>> m = datapoint.Manager(api_key = "blah")
        >>> f = m.get_forecast(latitude=50, longitude=0, frequency="hourly")
        >>> f.future(hours=26)


        :parameter days: How many days ahead
        :parameter hours: How many hours ahead
        :parameter minutes: How many minutes ahead
        :type days: int
        :type hours: int
        :type minutes: int

        :return: Individual forecast timestep
        :rtype: dict
        """

        d = datetime.datetime.now(tz=self.timesteps[0]["time"].tzinfo)
        target = d + datetime.timedelta(days=days, hours=hours, minutes=minutes)

        return self.at_datetime(target)
