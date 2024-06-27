from models.base_model import BaseModel
from db import db
from sqlalchemy import String, Column, Float, Integer, DateTime, func
import uuid

class City(BaseModel, db.Model):
    """ City class """

    __tablename__ = "cities"
    id = Column(String(256), nullable=False, default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column(String(128), nullable=False)
    country_id = Column(String(60), nullable=False)

    def __init__(self, name, country_id):
        """ Constructor for City"""
        super().__init__()
        self.name = name
        self.country_id = country_id
