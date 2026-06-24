from pydantic import BaseModel
from typing import List, Dict


class StudyTask(BaseModel):
    day: int
    task: str


class StudyPlanResponse(BaseModel):
    three_day_plan: List[Dict]
    seven_day_plan: List[Dict]
    thirty_day_plan: List[Dict]
