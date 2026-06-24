from pydantic import BaseModel
from typing import List, Dict, Any


class StudyTask(BaseModel):
    day: int
    task: str


class StudyPlanResponse(BaseModel):
    three_day_plan: List[Dict[str, Any]]
    seven_day_plan: List[Dict[str, Any]]
    thirty_day_plan: List[Dict[str, Any]]
