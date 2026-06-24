from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(256), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship('Resume', back_populates='user', cascade='all, delete-orphan')
    interviews = relationship('Interview', back_populates='user', cascade='all, delete-orphan')
    responses = relationship('Response', back_populates='user', cascade='all, delete-orphan')
    analytics = relationship('Analytics', back_populates='user', cascade='all, delete-orphan')
