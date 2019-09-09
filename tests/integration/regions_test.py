import os

from nose.tools import *
from requests import HTTPError

import datapoint


class TestRegions(object):
    def __init__(self):
        self.manager = datapoint.Manager(api_key=os.environ['NEW_API_KEY'])
        self.regions = self.manager.regions

    def test_key(self):
        assert self.regions.api_key == os.environ['NEW_API_KEY']

    def test_call_api(self):
        assert (
            u'RegionalFcst' in self.regions.call_api('/500'))
        assert_raises(
            HTTPError, self.regions.call_api, '/fake_path')
        assert_raises(
            HTTPError, self.regions.call_api, '/500', key='fake_key')

    def test_get_all_regions(self):
        all_regions = self.regions.get_all_regions()
        sample_region = next(
            region for region in all_regions
            if region.id == '515')
        assert (sample_region.name == 'UK')
        assert (sample_region.region == 'uk')

    def test_get_raw_forecast(self):
        sample_region = self.regions.get_all_regions()[0]
        response = self.regions.get_raw_forecast(
            sample_region.id)['RegionalFcst']
        assert (response['regionId'] == sample_region.region)

        # Based on what Datapoint serves at time of writing...
        forecast_periods = response['FcstPeriods']['Period']
        forecast_ids = [period['id'] for period in forecast_periods]
        expected_ids = ['day1to2', 'day3to5', 'day6to15', 'day16to30']
        assert (forecast_ids == expected_ids)
