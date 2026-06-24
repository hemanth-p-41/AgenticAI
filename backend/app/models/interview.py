from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import Base


class Interview(Base):
    __tablename__ = 'interviews'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    company = Column(String(256), nullable=False)
    role = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(64), default='active')
    meta = Column(JSON, default={})

    user = relationship('User', back_populates='interviews')
    questions = relationship('Question', back_populates='interview', cascade='all, delete-orphan')
