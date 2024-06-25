class Country():
    """Defines the class Country"""

    def __init__(self, name, code):
        """Initializes the class Country wth the following parameters:
        :param name: str - Name of the Country.
        :param code: str - The Country international code."""
        self.name = name
        self.code = code

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            result[key] = value
        return result
