from models.base_model import BaseModel
from db import db
from sqlalchemy import String, Column,ForeignKey
import uuid

class City(BaseModel, db.Model):
    """ City class """

    __tablename__ = "cities"
    id = Column(String(256), nullable=False, default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column(String(128), nullable=False)
    country_id = Column(String(60), ForeignKey('countries.id'), nullable=False)
    uniq_id = Column(String(60), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    def __init__(self, name, country_id):
        """ Constructor for City"""
        super().__init__()
        self.name = name
        self.country_id = country_id

    def to_dict(self):
        return {
            "name": self.name,
            "country_id": self.country_id,
            "uniq_id": self.uniq_id
        }