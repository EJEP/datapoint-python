import geojson
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from datapoint.exceptions import APIException
from datapoint.Forecast import Forecast

API_URL = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/"


class Manager:
    """Manager for DataHub connection.

    Wraps calls to DataHub API, and provides Forecast objects. Basic Usage:

    ::

      >>> import datapoint
      >>> m = datapoint.Manager.Manager(api_key = "blah")
      >>> f = m.get_forecast(
                  latitude=50,
                  longitude=0,
                  frequency="hourly",
                  convert_weather_code=True
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

    def __init__(self, api_key=""):
        self.api_key = api_key

    def __get_retry_session(
        self,
        retries=10,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
    ):
        """
        Retry the connection using requests if it fails. Use this as a wrapper
        to request from datapoint. See
        https://requests.readthedocs.io/en/latest/user/advanced/?highlight=retry#example-automatic-retries
        for more details.

        :parameter retries: How many times to retry
        :parameter backoff_factor: Backoff between attempts after second try
        :parameter status_forcelist: Codes to force a retry on
        :parameter session: Existing session to use

        :return: Session object
        :rtype: <class 'requests.sessions.Session'>
        """

        # requests.Session allows finer control, which is needed to use the
        # retrying code
        the_session = session or requests.Session()

        # The Retry object manages the actual retrying
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )

        adapter = HTTPAdapter(max_retries=retry)

        the_session.mount("http://", adapter)
        the_session.mount("https://", adapter)

        return the_session

    def __call_api(self, latitude, longitude, frequency):
        """
        Call the datapoint api using the requests module

        :parameter latitude: Latitude of forecast location
        :parameter longitude: Longitude of forecast location
        :parameter frequency: Forecast frequency. One of 'hourly', 'three-hourly, 'daily'
        :type latitude: float
        :type longitude: float
        :type frequency: string

        :return: Data from DataPoint
        :rtype: dict
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "includeLocationName": True,
            "excludeParameterMetadata": False,
        }
        headers = {
            "accept": "application/json",
            "apikey": self.api_key,
        }
        request_url = API_URL + frequency

        # Add a timeout to the request.
        # The value of 1 second is based on attempting 100 connections to
        # datapoint and taking ten times the mean connection time (rounded up).
        # Could expose to users in the functions which need to call the api.
        # req = requests.get(url, params=payload, timeout=1)
        # The wrapper function __retry_session returns a requests.Session
        # object. This has a .get() function like requests.get(), so the use
        # doesn't change here.

        sess = self.__get_retry_session()
        req = sess.get(
            request_url,
            params=params,
            headers=headers,
            timeout=1,
        )

        req.raise_for_status()

        try:
            data = geojson.loads(req.text)
        except ValueError as exc:
            raise APIException("DataPoint has not returned valid JSON") from exc

        return data

    def get_forecast(
        self, latitude, longitude, frequency="daily", convert_weather_code=True
    ):
        """
        Get a forecast for the provided site

        :parameter latitude: Latitude of forecast location
        :parameter longitude: Longitude of forecast location
        :parameter frequency: Forecast frequency. One of 'hourly', 'three-hourly, 'daily'
        :parameter convert_weather_code: Convert numeric weather codes to string description
        :type latitude: float
        :type longitude: float
        :type frequency: string
        :type convert_weather_code: bool

        :return: :class: `Forecast <Forecast>` object
        :rtype: datapoint.Forecast
        """
        if frequency not in ["hourly", "three-hourly", "daily"]:
            raise ValueError(
                "frequency must be set to one of 'hourly', 'three-hourly', 'daily'"
            )
        data = self.__call_api(latitude, longitude, frequency)
        forecast = Forecast(
            frequency=frequency,
            api_data=data,
            convert_weather_code=convert_weather_code,
        )

        return forecast
