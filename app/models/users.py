from models.base_model import BaseModel
from sqlalchemy import String, Column, Boolean, DateTime, func
from db import db
import uuid


class User(BaseModel, db.Model):
    """ User class """

    __tablename__ = "users"

    id = Column(String(256), nullable=False, default=lambda: str(uuid.uuid4()), primary_key=True)
    email = Column(String(256), nullable=False)
    first_name = Column(String(50), nullable = False)
    last_name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())

    def __init__(self, email, first_name, last_name, password):
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password


"""
curl -X POST http://localhost:5000/users \
     -H "Content-Type: application/json" \
     -d '{
           "email": "seth.s@example.com",
           "first_name": "Seth",
           "last_name": "S",
           "password": "seddssssss"
         }'

"""         