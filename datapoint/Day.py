class Day():
    def __init__(self):
        self.date = None
        self.timesteps = []

    def __str__(self):
        day_str = ''

        date_part = 'Date: ' + str(self.date) + '\n\n'
        day_str += date_part

        day_str += 'Timesteps: \n\n'
        try:
            for timestep in self.timesteps:
                day_str += str(timestep)
                day_str += '\n'

        except TypeError:
            day_str += 'No timesteps'

        return day_str
