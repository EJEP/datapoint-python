class Site():
    def __init__(self, api_key=""):
        self.api_key = api_key

        self.name = None
        self.id = None
        self.elevation = None
        self.latitude = None
        self.longitude = None
        self.nationalPark = None
        self.region = None
        self.unitaryAuthArea = None

    def __str__(self):
        site_string = ''
        for attr, value in self.__dict__.items():
            to_append = attr + ': ' + str(value) + '\n'
            site_string += to_append

        return site_string
