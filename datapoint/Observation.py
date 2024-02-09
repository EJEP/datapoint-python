class Observation():
    def __init__(self):
        self.data_date = None
        self.continent = None
        self.country = None
        self.name = None
        self.longitude = None
        self.latitude = None
        self.location_id = None
        self.elevation = None
        # Stores a list of observations in days
        self.days = []

    def now(self):
        """
        Return the final timestep available. This is the most recent
        observation.
        """

        return self.days[-1].timesteps[-1]
