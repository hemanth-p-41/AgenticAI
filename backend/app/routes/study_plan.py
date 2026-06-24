from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.routes.auth import get_current_user
from app.services.study_plan_service import StudyPlanService
from app.services.analytics_service import AnalyticsService
from app.schemas.study_plan import StudyPlanResponse

router = APIRouter(tags=['study-plan'])


@router.get('/me', response_model=StudyPlanResponse)
def me(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # detect weaknesses
    ana = AnalyticsService(db, user=current_user)
    weak = ana.weakness_detection().get('frequently_weak_categories', [])
    weak_cats = [c[0] for c in weak] if weak else ['PROJECTS']

    svc = StudyPlanService(db, current_user)
    plans = svc.generate_plans(weak_cats)
    return plans
