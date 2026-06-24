from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.routes.auth import get_current_user
from app.schemas.interview import (
    CreateInterviewRequest,
    CreateInterviewResponse,
    QuestionResponse,
    AnswerRequest,
    ProgressResponse,
)
from app.services.interview_service import InterviewService
from app.models.question import Question

router = APIRouter(tags=['interview'])


@router.post('/create', response_model=CreateInterviewResponse)
def create_interview(payload: CreateInterviewRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = InterviewService(db)
    try:
        interview = service.create_interview(current_user, payload.company, payload.role, payload.resume_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    qcount = db.query(Question).filter(Question.interview_id == interview.id).count()
    return CreateInterviewResponse(interview_id=interview.id, question_count=qcount)


@router.get('/{interview_id}/next', response_model=QuestionResponse)
def get_next(interview_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = InterviewService(db)
    question = service.get_next_question(interview_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No next question')
    return QuestionResponse(question_id=question.id, question=question.text)


@router.post('/answer')
def submit_answer(payload: AnswerRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = InterviewService(db)
    try:
        resp = service.submit_answer(current_user, payload.question_id, payload.answer)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {'status': 'saved'}


@router.get('/{interview_id}/progress', response_model=ProgressResponse)
def progress(interview_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = InterviewService(db)
    prog = service.get_progress(interview_id)
    return ProgressResponse(**prog)
