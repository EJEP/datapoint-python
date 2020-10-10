class Element():
    def __init__(self, id=None, value=None, units=None):

        self.id = id
        self.value = value
        self.units = units

        # For elements which can also have a text value
        self.text = None

    def __str__(self):
        return str(self.value) + ' ' + str(self.units)
