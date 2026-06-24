from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from .base import Base


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey('interviews.id', ondelete='CASCADE'), nullable=False)
    text = Column(Text, nullable=False)
    category = Column(String(128), nullable=True)
    meta = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    interview = relationship('Interview', back_populates='questions')
    responses = relationship('Response', back_populates='question', cascade='all, delete-orphan')
