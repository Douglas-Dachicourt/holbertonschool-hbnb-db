from models.base_model import BaseModel
from sqlalchemy import String, Column, Boolean, DateTime, func
from db import db
import uuid

class Amenity(BaseModel, db.Model):
    """ Amenity class """

    __tablename__ = "amenities"

    id = Column(String(256), nullable=False, default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column(String(128), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name
