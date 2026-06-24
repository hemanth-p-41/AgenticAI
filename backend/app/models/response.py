from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from .base import Base


class Response(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    interview_id = Column(Integer, ForeignKey('interviews.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    answer_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    evaluation = Column(JSON, nullable=True)

    question = relationship('Question', back_populates='responses')
    user = relationship('User', back_populates='responses')
