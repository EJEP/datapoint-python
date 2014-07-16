class Site(object):
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
