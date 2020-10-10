from .Element import Element

class Timestep():
    def __init__(self):
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

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def elements(self):
        """Return a list of the Elements which are not None"""
        elements = [el[1] for el in self.__dict__.items() if isinstance(el[1], Element)]

        return elements

    def __str__(self):
        timestep_string = ''
        for attr, value in self.__dict__.items():
            to_append = attr + ': ' + str(value) + '\n'
            timestep_string += to_append
        return timestep_string
