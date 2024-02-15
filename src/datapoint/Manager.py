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


class Manager:
    """
    Datapoint Manager object

    Wraps calls to DataHub API, and provides Forecast objects
    Basic Usage::

    >>> import datapoint
    >>> m = datapoint.Manager(api_key = "blah")
    >>> f = m.get_forecast(latitude=50, longitude=0, frequency="hourly")
    >>> f.now()
    <TBD>
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
        :rtype: TBD
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

        print(request_url)
        print(params)
        print(headers)
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

    def get_forecast(self, latitude, longitude, frequency="daily"):
        """
        Get a forecast for the provided site

        :parameter latitude: Latitude of forecast location
        :parameter longitude: Longitude of forecast location
        :parameter frequency: Forecast frequency. One of 'hourly', 'three-hourly, 'daily'
        :type latitude: float
        :type longitude: float
        :type frequency: string

        :return: :class: `Forecast <Forecast>` object
        :rtype: datapoint.Forecast
        """
        if frequency not in ["hourly", "three-hourly", "daily"]:
            raise ValueError(
                "frequency must be set to one of 'hourly', 'three-hourly', 'daily'"
            )
        data = self.__call_api(latitude, longitude, frequency)
        #with open('./hourly_api_data.json', 'w') as f:
        #    geojson.dump(data, f)
        forecast = Forecast(frequency=frequency, api_data=data)

        return forecast
