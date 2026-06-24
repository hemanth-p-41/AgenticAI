from pydantic import BaseModel
from typing import List, Optional


class EvaluationRequest(BaseModel):
    question_id: int
    answer: str


class EvaluationResponse(BaseModel):
    score: int
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    ideal_answer: str
    category: str


class BulkEvaluationResponse(BaseModel):
    average_score: float
    evaluated_questions: int


class InterviewSummaryResponse(BaseModel):
    average_score: float
    strongest_area: Optional[str]
    weakest_area: Optional[str]
    question_breakdown: List[dict]
