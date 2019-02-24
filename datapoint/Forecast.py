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

    def timedelta_total_seconds(self, timedelta):
        return (
            timedelta.microseconds + 0.0 +
            (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6

    def now(self):
        """
        Function to return just the current timestep from this forecast
        """

        # From the comments in issue 19: forecast.days[0] is dated for the
        # previous day shortly after midnight

        now = None
        d = datetime.datetime.utcnow()
        # d is something like datetime.datetime(2019, 1, 19, 17, 5, 28, 337439)
        # d.replace(...) is datetime.datetime(2019, 1, 19, 0, 0)
        # for_total_seconds is then: datetime.timedelta(seconds=61528,
        #                                               microseconds=337439)
        # In this example, this is (17*60*60) + (5*60) + 28 = 61528
        # this is the number of seconds through the day
        for_total_seconds = d - \
            d.replace(hour=0, minute=0, second=0, microsecond=0)

        # In the example time,
        # for_total_seconds.total_seconds() = 61528 + 0.337439
        # This is the number of seconds after midnight
        # msm is then the number of minutes after midnight
        msm = for_total_seconds.total_seconds() / 60

        # If the date now and the date in the forecast are the same, proceed
        if self.days[0].date.strftime("%Y-%m-%dZ") == d.strftime("%Y-%m-%dZ"):
            # We have determined that the date in the forecast and the date now
            # are the same.
            #
            # Now, test if timestep.name is larger than the number of minutes
            # since midnight for each timestep.
            # The timestep we keep is the one with the largest timestep.name
            # which is less than the number of minutes since midnight
            for timestep in self.days[0].timesteps:
                if timestep.name > msm:

                    # break here stops the for loop
                    break
                # now is assigned to the last timestep that did not break the
                # loop
                now = timestep
            return now
        # Bodge to get around problems near midnight:
        # If the date now is one day ahead of the date in the forecast, and the
        # time now is between 00:00 and 01:00 then also proceed.
        # Is the timestep.name > msm logic correct?
        # Likely not, want the last value
        elif self.days[0].date.day - d.date().day == -1 and d.time().hour < 1:
            # This is verbose to check that the returned data makes sense
            timestep_to_return = self.days[0].timesteps[-1]

            return timestep_to_return
        else:
            return False

    def future(self,in_days=None,in_hours=None,in_minutes=None,in_seconds=None):
        """
        Function to return a future timestep
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
                    future = timestep
                    return future
        else:
            print('ERROR: requested date is outside the forecast range selected,' + str(len(self.days)))
            return False
