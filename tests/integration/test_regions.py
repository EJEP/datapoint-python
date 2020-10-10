import os
from requests import HTTPError
import unittest
import datapoint


class RegionsIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.manager = datapoint.Manager(api_key=os.environ['API_KEY'])
        self.regions = self.manager.regions

    def test_key(self):
        self.assertEqual(self.regions.api_key, os.environ['API_KEY'])

    def test_call_api(self):
        self.assertIn (
            u'RegionalFcst', self.regions.call_api('/500'))
        self.assertRaises(
            HTTPError, self.regions.call_api, '/fake_path')
        self.assertRaises(
            HTTPError, self.regions.call_api, '/500', key='fake_key')

    def test_get_all_regions(self):
        all_regions = self.regions.get_all_regions()
        sample_region = next(
            region for region in all_regions
            if region.location_id == '515')
        self.assertEqual(sample_region.name, 'UK')
        self.assertEqual(sample_region.region, 'uk')

    def test_get_raw_forecast(self):
        sample_region = self.regions.get_all_regions()[0]
        response = self.regions.get_raw_forecast(
            sample_region.location_id)['RegionalFcst']
        self.assertEqual(response['regionId'], sample_region.region)

        # Based on what Datapoint serves at time of writing...
        forecast_periods = response['FcstPeriods']['Period']
        forecast_ids = [period['id'] for period in forecast_periods]
        expected_ids = ['day1to2', 'day3to5', 'day6to15', 'day16to30']
        self.assertEqual(forecast_ids, expected_ids)
