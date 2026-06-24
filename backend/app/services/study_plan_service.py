from typing import Dict, List
from app.services.gemini_service import GeminiService


class StudyPlanService:
    def __init__(self, db, user):
        self.db = db
        self.user = user
        self.gemini = GeminiService()

    def _deterministic_plan_for_category(self, category: str, days: int) -> List[Dict]:
        # Simple deterministic tasks per category
        tasks = []
        for d in range(1, days + 1):
            tasks.append({'day': d, 'task': f"Day {d}: Study {category} topic {d} - read concept and do 1 exercise."})
        return tasks

    def generate_plans(self, weaknesses: List[str]) -> Dict[str, List[Dict]]:
        # weaknesses is list of category strings
        three = []
        seven = []
        thirty = []
        if self.gemini.enabled:
            # Placeholder for calling Gemini to generate personalized plans
            raise NotImplementedError('Gemini study plan integration not implemented')

        # deterministic: pick top 2 weaknesses and distribute tasks
        top = weaknesses[:2] if weaknesses else ['PROJECTS']
        for cat in top:
            three.extend(self._deterministic_plan_for_category(cat, 3))
            seven.extend(self._deterministic_plan_for_category(cat, 7))
            thirty.extend(self._deterministic_plan_for_category(cat, 30))

        return {'three_day_plan': three, 'seven_day_plan': seven, 'thirty_day_plan': thirty}
