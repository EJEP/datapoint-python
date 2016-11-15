import datetime
import sys

class Forecast(object):
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
        self.days = []

    def timedelta_total_seconds(self, timedelta):
        return (
            timedelta.microseconds + 0.0 +
            (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

    def now(self):
        """
        Function to return just the current timestep from this forecast
        """
        now = None
        d = datetime.datetime.utcnow()
        for_total_seconds = d - d.replace(hour=0, minute=0, second=0, microsecond=0)
        # python 2.6 does not have timedelta.total_seconds()
        if sys.version_info < (2,7):
            msm = self.timedelta_total_seconds(for_total_seconds) / 60
        else:
            msm = for_total_seconds.total_seconds() / 60
        if self.days[0].date.strftime("%Y-%m-%dZ") == d.strftime("%Y-%m-%dZ"):
            for timestep in self.days[0].timesteps:
                if timestep.name > msm:
                    break
                now = timestep
            return now
        else:
            return False
