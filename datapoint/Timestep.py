class Timestep(object):
    def __init__(self, api_key=""):
        self.api_key = api_key

        self.name = None
        self.date = None
        self.weather = None
        self.temperature = None
        self.feels_like_temperature = None
        self.wind_speed = None
        self.wind_direction = None
        self.wind_gust = None
        self.visibility = None
        self.uv = None
        self.precipitation = None
        self.humidity = None
        self.pressure = None
        self.pressure_tendency = None
        self.dew_point = None

    def elements(self):
        """Return a list of all the elements"""

        elements = [
            self.weather,
            self.temperature,
            self.feels_like_temperature,
            self.wind_speed,
            self.wind_direction,
            self.wind_gust,
            self.visibility,
            self.uv,
            self.precipitation,
            self.humidity,
            self.pressure,
            self.pressure_tendency,
            self.dew_point,]

        return elements
