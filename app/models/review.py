from models.base_model import BaseModel


class Review(BaseModel):
    """Defines a class Review that inherits from BaseModel"""

    def __init__(self, user_id, place_id, rating, comment):
        """Initialzes the class Review with the following parmeters:
        :param user_id: UUID - Unique ID of an User.
        :param place_id: UUID - Unique ID of a Place.
        :param rating: int - rating given to a Place by an User.
        :param comment: str - comment given to a Place by an User."""
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment
