from models.base_model import BaseModel


class Place(BaseModel):
    """Defines class Place that inherits from BaseModel"""

    def __init__(self, name, description, address, city_id, latitude,
                 longitude, host_id, num_rooms, num_bathrooms,
                 price_per_night, max_guests, amenity_ids):
        """Initializes the class Place with the following parameters:
        :param name: str - name of the place.
        :param description: star - a description of the place.
        :param address: str - the adress of the place.
        :param city_id: UUID - Unique ID of the City the Place is in.
        :param lattitude: float - the lattitude at wich the Place is.
        :param longitude: float - the longitude at wich the Place is.
        :param host_id: UUID - Unique ID of the owner of the Place.
        :param num_room: int -  number of room the Place is composed of.
        :param num_bathrooms: int - number of bathroom in the Place.
        :param price_per_night: float - price of the Place, per night.
        :param max_guests: int - number of guests the Place can accept.
        """
        super().__init__()
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.num_rooms = num_rooms
        self.num_bathrooms = num_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenity_ids = amenity_ids
