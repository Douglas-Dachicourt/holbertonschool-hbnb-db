from sqlalchemy import String, Column, Integer
from db import db

class Country(db.Model):
    """Defines the class Country"""

    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    code = Column(String(10), nullable=False)


    def __init__(self, name, code):
        """Initializes the class Country wth the following parameters:
        :param name: str - Name of the Country.
        :param code: str - The Country international code."""
        self.name = name
        self.code = code

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code
        }
