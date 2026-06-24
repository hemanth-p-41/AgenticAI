from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.routes.auth import get_current_user
from app.schemas.evaluation import (
    EvaluationRequest,
    EvaluationResponse,
    BulkEvaluationResponse,
    InterviewSummaryResponse,
)
from app.services.evaluation_service import EvaluationService

router = APIRouter(tags=['evaluation'])


@router.post('/', response_model=EvaluationResponse)
def evaluate(payload: EvaluationRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = EvaluationService(db)
    try:
        ev = service.evaluate_answer(payload.question_id, payload.answer, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return EvaluationResponse(**ev)


@router.post('/interview/{interview_id}', response_model=BulkEvaluationResponse)
def bulk_evaluate(interview_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = EvaluationService(db)
    res = service.bulk_evaluate_interview(interview_id, current_user)
    return BulkEvaluationResponse(**res)


@router.get('/interview/{interview_id}', response_model=InterviewSummaryResponse)
def summary(interview_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = EvaluationService(db)
    res = service.interview_summary(interview_id)
    return InterviewSummaryResponse(**res)
