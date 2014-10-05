import datetime

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

    def now(self):
        """
        Function to return just the current timestep from this forecast
        """
        now = None
        d = datetime.datetime.utcnow()
        msm = (d - d.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() / 60
        if self.days[0].date == d.strftime("%Y-%m-%dZ"):
            for timestep in self.days[0].timesteps:
                if timestep.name > msm:
                    break
                now = timestep
            return now
        else:
            return False
