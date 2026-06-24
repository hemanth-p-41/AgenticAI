from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class ResumeAnalysis(BaseModel):
    skills: List[str] = []
    projects: List[str] = []
    technologies: List[str] = []
    achievements: List[str] = []


class ResumeCreateResponse(BaseModel):
    id: int
    filename: str
    file_path: str

    model_config = {"from_attributes": True}


class ResumeResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    extracted_text: Optional[str]
    uploaded_at: datetime
    analysis: ResumeAnalysis

    model_config = {"from_attributes": True}
