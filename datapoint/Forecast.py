import datetime
from datapoint.exceptions import APIException

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

    def at_datetime(self, target):
        """ Return the timestep closest to the target datetime"""

        # Convert target to offset aware datetime
        if target.tzinfo is None:
            target = datetime.datetime.combine(target.date(), target.time(), self.days[0].date.tzinfo)

        num_timesteps = len(self.days[1].timesteps)
        # First check that the target is at most 1.5 hours before the first timestep
        if target < self.days[0].timesteps[0].date - datetime.timedelta(hours=1, minutes=30) and num_timesteps == 8:
            err_str = 'There is no forecast available for the requested time. ' + \
                'The requested time is more than 1.5 hours before the first available forecast'
            raise APIException(err_str)

        elif target < self.days[0].timesteps[0].date - datetime.timedelta(hours=6) and num_timesteps == 2:

            err_str = 'There is no forecast available for the requested time. ' + \
                'The requested time is more than 6 hours before the first available forecast'

            raise APIException(err_str)

        # Ensure that the target is less than 1 hour 30 minutes after the final
        # timestep.
        # Logic is correct
        # If there are 8 timesteps per day, then the target must be within 1.5
        # hours of the last timestep
        if target > (self.days[-1].timesteps[-1].date + datetime.timedelta(hours=1, minutes=30)) and num_timesteps == 8:

            err_str = 'There is no forecast available for the requested time. The requested time is more than 1.5 hours after the first available forecast'

            raise APIException(err_str)

        # If there are 2 timesteps per day, then the target must be within 6
        # hours of the last timestep
        if target > (self.days[-1].timesteps[-1].date + datetime.timedelta(hours=6)) and num_timesteps == 2:

            err_str = 'There is no forecast available for the requested time. The requested time is more than 6 hours after the first available forecast'

            raise APIException(err_str)

        # Loop over all timesteps
        # Calculate the first time difference
        prev_td = target - self.days[0].timesteps[0].date
        prev_ts = self.days[0].timesteps[0]

        for day in self.days:
            for timestep in day.timesteps:
                # Calculate the difference between the target time and the timestep.
                td = target - timestep.date

                # Find the timestep which is further from the target than the
                # previous one. Return the previous timestep
                if abs(td.total_seconds()) > abs(prev_td.total_seconds()):
                    # We are further from the target
                    return prev_ts
                elif abs(td.total_seconds()) < 5400 and num_timesteps == 8:
                    # if we are past the final timestep, and it is a 3 hourly
                    # forecast, check that we are within 90 minutes of it
                    return timestep
                elif abs(td.total_seconds()) < 21600 and num_timesteps == 2:
                    # if we are past the final timestep, and it is a daily
                    # forecast, check that we are within 6 hours of it
                    return timestep

                prev_ts = timestep
                prev_td = td

    def now(self):
        """Function to return the closest timestep to the current time
        """

        d = datetime.datetime.now(tz=self.days[0].date.tzinfo)
        return self.at_datetime(d)

    def now_old(self):
        """
        Function to return just the current timestep from this forecast
        """

        # From the comments in issue 19: forecast.days[0] is dated for the
        # previous day shortly after midnight

        now = None
        # Set the time now to be in the same time zone as the first timestep in
        # the forecast. This shouldn't cause problems with daylight savings as
        # the change is far enough after midnight.
        d = datetime.datetime.now(tz=self.days[0].date.tzinfo)
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
        # Previous method does not account for the end of the month. The test
        # trying to be evaluated is that the absolute difference between the
        # last timestep of the first day and the current time is less than 4
        # hours. 4 hours is because the final timestep of the previous day is
        # for 21:00
        elif abs(self.days[0].timesteps[-1].date - d).total_seconds() < 14400:
            # This is verbose to check that the returned data makes sense
            timestep_to_return = self.days[0].timesteps[-1]

            return timestep_to_return
        else:
            return False


    def future(self,in_days=0,in_hours=0,in_minutes=0,in_seconds=0):
        """Return the closest timestep to a date in a given amount of time"""

        d = datetime.datetime.now(tz=self.days[0].date.tzinfo)
        target = d + datetime.timedelta(days=in_days, hours=in_hours,
                                        minutes=in_minutes, seconds=in_seconds)

        return self.at_datetime(target)

    def future_old(self,in_days=None,in_hours=None,in_minutes=None,in_seconds=None):
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
