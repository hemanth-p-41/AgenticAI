from pydantic import BaseModel
from typing import Dict, Optional, List, Any


class UserAnalyticsResponse(BaseModel):
    overall_score: float
    strongest_area: Optional[str]
    weakest_area: Optional[str]
    categories: Dict[str, float]


class TrendsResponse(BaseModel):
    history: List[float]
    improvement: float


class WeaknessDetectionResponse(BaseModel):
    frequently_weak_categories: List[str]
    repeated_weaknesses: List[str]
