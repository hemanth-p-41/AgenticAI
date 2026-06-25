from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ResumeAnalysis(BaseModel):
    skills: List[str] = []
    projects: List[str] = []
    technologies: List[str] = []
    achievements: List[str] = []


class ResumeCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    file_path: str


class ResumeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    file_path: str
    extracted_text: Optional[str]
    uploaded_at: datetime
    analysis: ResumeAnalysis
