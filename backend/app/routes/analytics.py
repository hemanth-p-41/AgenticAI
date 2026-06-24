from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.routes.auth import get_current_user
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import UserAnalyticsResponse, TrendsResponse, WeaknessDetectionResponse

router = APIRouter(tags=['analytics'])


@router.get('/me', response_model=UserAnalyticsResponse)
def me(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    svc = AnalyticsService(db, user=current_user)
    return svc.category_analytics()


@router.get('/trends', response_model=TrendsResponse)
def trends(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    svc = AnalyticsService(db, user=current_user)
    return svc.trends()


@router.get('/weaknesses', response_model=WeaknessDetectionResponse)
def weaknesses(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    svc = AnalyticsService(db, user=current_user)
    return svc.weakness_detection()
