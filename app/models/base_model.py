import uuid
from datetime import datetime
from flask import jsonify
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime

Base = declarative_base()


class BaseModel(Base):
    """ Base class for all models """

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    uniq_id = Column(String(256), unique=True, nullable=False,
                     default=str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    def save(self):
        from app import db

        db.session.add(self)
        db.session.commit()

    def delete(self):
        from app import db

        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime.datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
