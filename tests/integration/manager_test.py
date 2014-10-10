import os
from types import *
from nose.tools import *

import datapoint

class TestManager:

    def __init__(self):
        self.manager = datapoint.Manager(api_key=os.environ['API_KEY'])

    def test_site(self):
        site = self.manager.get_nearest_site(-0.124626, 51.500728)
        assert site.name == 'London'

