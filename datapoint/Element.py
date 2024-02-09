class Element():
    def __init__(self, field_code=None, value=None, units=None):

        self.field_code = field_code
        self.value = value
        self.units = units

        # For elements which can also have a text value
        self.text = None

    def __str__(self):
        return str(self.value) + ' ' + str(self.units)
