from pydantic import BaseModel
from typing import Optional


class CreateInterviewRequest(BaseModel):
    company: str
    role: str
    resume_id: int


class CreateInterviewResponse(BaseModel):
    interview_id: int
    question_count: int


class QuestionResponse(BaseModel):
    question_id: int
    question: str


class AnswerRequest(BaseModel):
    question_id: int
    answer: str


class ProgressResponse(BaseModel):
    answered: int
    remaining: int
    completion_percentage: int
