from models.base_model import BaseModel


class Amenity(BaseModel):
    """ Amenity class """

    def __init__(self, name):
        super().__init__()
        self.name = name
