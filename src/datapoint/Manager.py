"""
Datapoint python module
"""

import geojson
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from datapoint.exceptions import APIException
from datapoint.Forecast import Forecast

API_URL = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/"
DATE_FORMAT = "%Y-%m-%dZ"
DATA_DATE_FORMAT = "%Y-%m-%dT%XZ"
FORECAST_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class Manager:
    """
    Datapoint Manager object
    """

    def __init__(self, api_key=""):
        self.api_key = api_key
        self.call_response = None

    def __retry_session(
        self,
        retries=10,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
    ):
        """
        Retry the connection using requests if it fails. Use this as a wrapper
        to request from datapoint
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

        sess = self.__retry_session()
        req = sess.get(
            request_url,
            params=params,
            headers=headers,
            timeout=1,
        )

        try:
            data = geojson.loads(req.text)
        except ValueError as exc:
            raise APIException(
                "DataPoint has not returned any data, this could be due to an incorrect API key"
            ) from exc
        self.call_response = data
        if req.status_code != 200:
            msg = [
                data[m] for m in ("message", "error_message", "status") if m in data
            ][0]
            raise Exception(msg)
        return data

    def _visibility_to_text(self, distance):
        """
        Convert observed visibility in metres to text used in forecast
        """

        if not isinstance(distance, int):
            raise ValueError("Distance must be an integer not", type(distance))
        if distance < 0:
            raise ValueError("Distance out of bounds, should be 0 or greater")

        if 0 <= distance < 1000:
            return "VP"
        elif 1000 <= distance < 4000:
            return "PO"
        elif 4000 <= distance < 10000:
            return "MO"
        elif 10000 <= distance < 20000:
            return "GO"
        elif 20000 <= distance < 40000:
            return "VG"
        else:
            return "EX"

    def get_forecast(self, latitude, longitude, frequency="daily"):
        """
        Get a forecast for the provided site

        A frequency of "daily" will return two timesteps:
        "Day" and "Night".

        A frequency of "3hourly" will return 8 timesteps:
        0, 180, 360 ... 1260 (minutes since midnight UTC)
        """
        if frequency not in ["hourly", "three-hourly", "daily"]:
            raise ValueError(
                "frequency must be set to one of 'hourly', 'three-hourly', 'daily'"
            )
        data = self.__call_api(latitude, longitude, frequency)
        # print(data)
        forecast = Forecast(frequency=frequency, api_data=data)

        return forecast
