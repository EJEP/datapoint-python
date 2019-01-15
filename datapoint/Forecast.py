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
        for_total_seconds = d - \
            d.replace(hour=0, minute=0, second=0, microsecond=0)
        # python 2.6 does not have timedelta.total_seconds()
        if sys.version_info < (2,7):
            msm = self.timedelta_total_seconds(for_total_seconds) / 60
        else:
            msm = for_total_seconds.total_seconds() / 60
        # If the date now and the date in the forecast are the same, proceed
        if self.days[0].date.strftime("%Y-%m-%dZ") == d.strftime("%Y-%m-%dZ"):
            print("Here")
            print("msm: " + str(msm))
            for timestep in self.days[0].timesteps:
                print(timestep.name)
                if timestep.name > msm:
                    #print timestep.date,timestep.name,msm
                    now = timestep
                    print(now)
                    return now
        # Bodge to get around problems near midnight:
        # If the date now is one day ahead of the date in the forecast, and the
        # time now is between 00:00 and 01:00 then also proceed.
        #elif self.days[0].date().day - d.date().day and d.time().minute < 60:
        #     for timestep in self.days[0].timesteps:
        #        if timestep.name > msm:
                    #print timestep.date,timestep.name,msm
        #             now = timestep
        #             return now
        else:
            return False

    def future(self,in_days=None,in_hours=None,in_minutes=None,in_seconds=None):
        """
        Function to return a future timestp 
        """
        future = None

        # Initialize variables to 0
        dd, hh, mm, ss = [0 for i in range(4)]
        if (in_days != None):
            dd = dd + in_days
        if (in_hours != None):
            hh = hh + in_hours
        if (in_minutes != None):
            mm = mm + in_minutes
        if (in_seconds != None):
            ss = ss + in_seconds
        #print dd,hh,mm,ss
            
        # Set the hours, minutes and seconds from now (minus the days)
        dnow = datetime.datetime.utcnow()  # Now
        d = dnow + \
            datetime.timedelta(hours=hh, minutes=mm, seconds = ss)
        # Time from midnight
        for_total_seconds = d - \
            d.replace(hour=0, minute=0, second=0, microsecond=0)  

        # Convert into minutes since midnight
        try:
            msm = for_total_seconds.total_seconds()/60.
        except:
            # For versions before 2.7
            msm = self.timedelta_total_seconds(for_total_seconds)/60.

        if (dd<len(self.days)):
            for timestep in self.days[dd].timesteps:
                if timestep.name >= msm:
                    #print timestep.date,timestep.name,msm
                    future = timestep
                    return future
        else:
            print('ERROR: requested date is outside the forecast range selected,' + str(len(self.days)))
            return False
