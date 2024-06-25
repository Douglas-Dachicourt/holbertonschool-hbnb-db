from models.base_model import BaseModel
from sqlalchemy import String, Column, Boolean, DateTime, func
from app import db


class User(BaseModel, db.Model):
    """ User class """

    __tablename__ = "users"

    id = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False)
    password = Column(String(50), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())

    def __init__(self, email, first_name, last_name):
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
