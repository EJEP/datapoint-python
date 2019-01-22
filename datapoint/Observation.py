import datetime
import sys

class Observation(object):
    def __init__(self, api_key=""):
        self.api_key = api_key

        self.data_date = None
        self.continent = None
        self.country = None
        self.name = None
        self.longitude = None
        self.latitude = None
        self.id = None
        self.elevation = None
        # Stores a list of observations in days
        self.days = []

    # TODO: Add functions to get the latest observation and previous ones.
    # We always want the final day in the list of days, and the final timestep
    # in that day.

    def now(self):
        """
        Return the final timestep available.
        """

        return self.days[-1].timesteps[-1]
