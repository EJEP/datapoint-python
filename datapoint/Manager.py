"""
Datapoint python module
"""

from datetime import datetime
from datetime import timedelta
import sys
from time import time
import pytz

import requests

from .Site import Site
from .Forecast import Forecast
from .Day import Day
from .Timestep import Timestep
from .Element import Element

if (sys.version_info > (3, 0)):
    long = int

API_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json"
DATE_FORMAT = "%Y-%m-%dZ"
DATA_DATE_FORMAT = "%Y-%m-%dT%XZ"
FORECAST_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
ELEMENTS = {
    "Day":
        {"U":"U", "V":"V", "W":"W", "T":"Dm", "S":"S", "Pp":"PPd",
        "H":"Hn", "G":"Gn", "F":"FDm", "D":"D"},
    "Night":
        {"V":"V", "W":"W", "T":"Nm", "S":"S", "Pp":"PPn",
        "H":"Hm", "G":"Gm", "F":"FNm", "D":"D"},
    "Default":
        {"V":"V", "W":"W", "T":"T", "S":"S", "Pp":"Pp",
        "H":"H", "G":"G", "F":"F", "D":"D", "U":"U"}
}

WEATHER_CODES = {
    "0":"Clear night",
    "1":"Sunny day",
    "2":"Partly cloudy (night)",
    "3":"Partly cloudy (day)",
    "4":"Not used",
    "5":"Mist",
    "6":"Fog",
    "7":"Cloudy",
    "8":"Overcast",
    "9":"Light rain shower (night)",
    "10":"Light rain shower (day)",
    "11":"Drizzle",
    "12":"Light rain",
    "13":"Heavy rain shower (night)",
    "14":"Heavy rain shower (day)",
    "15":"Heavy rain",
    "16":"Sleet shower (night)",
    "17":"Sleet shower (day)",
    "18":"Sleet",
    "19":"Hail shower (night)",
    "20":"Hail shower (day)",
    "21":"Hail",
    "22":"Light snow shower (night)",
    "23":"Light snow shower (day)",
    "24":"Light snow",
    "25":"Heavy snow shower (night)",
    "26":"Heavy snow shower (day)",
    "27":"Heavy snow",
    "28":"Thunder shower (night)",
    "29":"Thunder shower (day)",
    "30":"Thunder"
}

class Manager(object):
    """
    Datapoint Manager object
    """

    def __init__(self, api_key=""):
        self.api_key = api_key
        self.call_response = None

        # The list of sites changes infrequently so limit to requesting it
        # every hour.
        self.sites_last_update = 0
        self.sites_last_request = None
        self.sites_update_time = 3600

    def __call_api(self, path, params=None):
        """
        Call the datapoint api using the requests module
        """
        if not params:
            params = dict()
        payload = {'key': self.api_key}
        payload.update(params)
        url = "%s/%s" % (API_URL, path)
        req = requests.get(url, params=payload)
        try:
            data = req.json()
        except ValueError:
            raise Exception("DataPoint has not returned any data, this could be due to an incorrect API key")
        self.call_response = data
        if req.status_code != 200:
            msg = [data[m] for m in ("message", "error_message", "status") \
                      if m in data][0]
            raise Exception(msg)
        return data

    def _distance_between_coords(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        distance = abs(lon1-lon2) + abs(lat1-lat2)
        return distance

    def _get_wx_units(self, params, name):
        """
        Give the Wx array returned from datapoint and an element
        name and return the units for that element.
        """
        units = ""
        for param in params:
            if str(name) == str(param['name']):
                units = param['units']
        return units

    def _weather_to_text(self, code):
        if not isinstance(code, (int, long)):
            raise ValueError("Weather code must be an integer not", type(code))
        if code < 0 or code > 30:
            raise ValueError("Weather code outof bounds, should be 0-30")
        text = WEATHER_CODES[str(code)]
        return text

    def get_all_sites(self):
        """
        This function returns a list of Site object.
        """
        if (time() - self.sites_last_update) > self.sites_update_time:
            self.sites_last_update = time()
            data = self.__call_api("sitelist/")
            sites = list()
            for jsoned in data['Locations']['Location']:
                site = Site()
                site.name = jsoned['name']
                site.id = jsoned['id']
                site.latitude = jsoned['latitude']
                site.longitude = jsoned['longitude']

                if 'region' in jsoned:
                    site.region = jsoned['region']

                if 'elevation' in jsoned:
                    site.elevation = jsoned['elevation']

                if 'unitaryAuthArea' in jsoned:
                    site.elevation = jsoned['unitaryAuthArea']

                if 'nationalPark' in jsoned:
                    site.elevation = jsoned['nationalPark']

                site.api_key = self.api_key

                sites.append(site)
            self.sites_last_request = sites
        else:
            sites = self.sites_last_request

        return sites

    def get_nearest_site(self, longitude=False, latitude=False):
        """
        This function returns the nearest Site object to the specified
        coordinates.
        """
        if not longitude or not latitude:
            return False

        nearest = False
        distance = False
        sites = self.get_all_sites()
        for site in sites:
            new_distance = \
                self._distance_between_coords(
                    float(site.longitude),
                    float(site.latitude),
                    float(longitude),
                    float(latitude))

            if new_distance < distance or not distance:
                distance = new_distance
                nearest = site
        return nearest

    def get_forecast_for_site(self, site_id, frequency="daily"):
        """
        Get a forecast for the provided site

        A frequency of "daily" will return two timesteps:
        "Day" and "Night".

        A frequency of "3hourly" will return 8 timesteps:
        0, 180, 360 ... 1260 (minutes since midnight UTC)
        """
        data = self.__call_api(site_id, {"res":frequency})
        params = data['SiteRep']['Wx']['Param']

        forecast = Forecast()
        forecast.data_date = data['SiteRep']['DV']['dataDate']
        forecast.data_date = datetime.strptime(data['SiteRep']['DV']['dataDate'], DATA_DATE_FORMAT).replace(tzinfo=pytz.UTC)
        forecast.continent = data['SiteRep']['DV']['Location']['continent']
        forecast.country = data['SiteRep']['DV']['Location']['country']
        forecast.name = data['SiteRep']['DV']['Location']['name']
        forecast.longitude = data['SiteRep']['DV']['Location']['lon']
        forecast.latitude = data['SiteRep']['DV']['Location']['lat']
        forecast.id = data['SiteRep']['DV']['Location']['i']
        forecast.elevation = data['SiteRep']['DV']['Location']['elevation']

        for day in data['SiteRep']['DV']['Location']['Period']:
            new_day = Day()
            new_day.date = datetime.strptime(day['value'], DATE_FORMAT).replace(tzinfo=pytz.UTC)

            for timestep in day['Rep']:
                new_timestep = Timestep()

                if timestep['$'] == "Day":
                    cur_elements = ELEMENTS['Day']
                    new_timestep.date = datetime.strptime(day['value'], DATE_FORMAT).replace(tzinfo=pytz.UTC) \
                                        + timedelta(hours=12)
                elif timestep['$'] == "Night":
                    cur_elements = ELEMENTS['Night']
                    new_timestep.date = datetime.strptime(day['value'], DATE_FORMAT).replace(tzinfo=pytz.UTC)
                else:
                    cur_elements = ELEMENTS['Default']
                    new_timestep.date = datetime.strptime(day['value'], DATE_FORMAT).replace(tzinfo=pytz.UTC) \
                                        + timedelta(minutes=int(timestep['$']))

                if frequency == 'daily':
                    new_timestep.name = timestep['$']
                elif frequency == '3hourly':
                    new_timestep.name = int(timestep['$'])

                new_timestep.weather = \
                    Element(cur_elements['W'],
                            timestep[cur_elements['W']],
                            self._get_wx_units(params, cur_elements['W']))
                new_timestep.weather.text = self._weather_to_text(int(timestep[cur_elements['W']]))

                new_timestep.temperature = \
                    Element(cur_elements['T'],
                            int(timestep[cur_elements['T']]),
                            self._get_wx_units(params, cur_elements['T']))

                new_timestep.feels_like_temperature = \
                    Element(cur_elements['F'],
                            int(timestep[cur_elements['F']]),
                            self._get_wx_units(params, cur_elements['F']))

                new_timestep.wind_speed = \
                    Element(cur_elements['S'],
                            int(timestep[cur_elements['S']]),
                            self._get_wx_units(params, cur_elements['S']))

                new_timestep.wind_direction = \
                    Element(cur_elements['D'],
                            timestep[cur_elements['D']],
                            self._get_wx_units(params, cur_elements['D']))

                new_timestep.wind_gust = \
                    Element(cur_elements['G'],
                            int(timestep[cur_elements['G']]),
                            self._get_wx_units(params, cur_elements['G']))

                new_timestep.visibility = \
                    Element(cur_elements['V'],
                            timestep[cur_elements['V']],
                            self._get_wx_units(params, cur_elements['V']))

                new_timestep.precipitation = \
                    Element(cur_elements['Pp'],
                            int(timestep[cur_elements['Pp']]),
                            self._get_wx_units(params, cur_elements['Pp']))

                new_timestep.humidity = \
                    Element(cur_elements['H'],
                            int(timestep[cur_elements['H']]),
                            self._get_wx_units(params, cur_elements['H']))

                if 'U' in cur_elements and cur_elements['U'] in timestep:
                    new_timestep.uv = \
                        Element(cur_elements['U'],
                                timestep[cur_elements['U']],
                                self._get_wx_units(params, cur_elements['U']))

                new_day.timesteps.append(new_timestep)
            forecast.days.append(new_day)

        return forecast
