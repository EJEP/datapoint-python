import json
from time import time

import requests

from datapoint.Site import Site
from datapoint.regions.region_names import REGION_NAMES
REGIONS_BASE_URL = 'http://datapoint.metoffice.gov.uk/public/data/txt/wxfcs/regionalforecast/json'


class RegionManager(object):
    '''
    Datapoint Manager for national and regional text forecasts
    '''
    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.all_regions_path = '/sitelist'
        if not base_url:
            self.base_url = REGIONS_BASE_URL

        # The list of regions changes infrequently so limit to requesting it
        # every hour.
        self.regions_last_update = 0
        self.regions_last_request = None
        self.regions_update_time = 3600

    def call_api(self, path, **kwargs):
        '''
        Call datapoint api
        '''
        if 'key' not in kwargs:
            kwargs['key'] = self.api_key
        req = requests.get('{0}{1}'.format(self.base_url, path), params=kwargs)

        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        return req.json()

    def get_all_regions(self):
        '''
        Request a list of regions from Datapoint. Returns each Region
        as a Site object. Regions rarely change, so we cache the response
        for one hour to minimise requests to API.
        '''
        if (time() - self.regions_last_update) < self.regions_update_time:
            return self.regions_last_request

        response = self.call_api(self.all_regions_path)
        regions = []
        for location in response['Locations']['Location']:
            region = Site()
            region.id = location['@id']
            region.region = location['@name']
            region.name = REGION_NAMES[location['@name']]
            regions.append(region)

        self.regions_last_update = time()
        self.regions_last_request = regions
        return regions

    def get_raw_forecast(self, region_id):
        '''
        Request unformatted forecast for a specific region_id.
        '''
        return self.call_api('/{0}'.format(region_id))
