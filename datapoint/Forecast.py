import datetime
from datapoint.exceptions import APIException


class Forecast():
    def __init__(self, api_key="", frequency=""):
        self.api_key = api_key

        self.frequency = frequency
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
                # Calculate the difference between the target time and the
                # timestep.
                td = target - timestep.date

                # Find the timestep which is further from the target than the
                # previous one. Return the previous timestep
                if abs(td.total_seconds()) > abs(prev_td.total_seconds()):
                    # We are further from the target
                    return prev_ts
                if abs(td.total_seconds()) < 5400 and num_timesteps == 8:
                    # if we are past the final timestep, and it is a 3 hourly
                    # forecast, check that we are within 90 minutes of it
                    return timestep
                if abs(td.total_seconds()) < 21600 and num_timesteps == 2:
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

    def future(self, in_days=0, in_hours=0, in_minutes=0, in_seconds=0):
        """Return the closest timestep to a date in a given amount of time"""

        d = datetime.datetime.now(tz=self.days[0].date.tzinfo)
        target = d + datetime.timedelta(days=in_days, hours=in_hours,
                                        minutes=in_minutes, seconds=in_seconds)

        return self.at_datetime(target)
