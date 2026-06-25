from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import Any
from app.database.session import get_db
from app.routes.auth import get_current_user
from app.services.resume_service import ResumeService
from app.schemas.resume import ResumeCreateResponse, ResumeResponse, ResumeAnalysis
from app.models.resume import Resume
from pathlib import Path

router = APIRouter(tags=['resume'])


@router.post('/upload', response_model=ResumeCreateResponse)
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> Any:
    # Validate content type
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail='Only PDF files are accepted')

    # Validate size (readable via UploadFile.file)
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail='File too large (max 10MB)')

    resume = ResumeService.create_resume(db, current_user.id, file)

    return ResumeCreateResponse.model_validate(resume)


@router.get('/{resume_id}', response_model=ResumeResponse)
def get_resume(resume_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> Any:
    resume = db.get(Resume, resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Resume not found')

    analysis = ResumeService.analyze_text(resume.extracted_text or '')
    return ResumeResponse(
        id=resume.id,
        filename=resume.filename,
        file_path=resume.file_path,
        extracted_text=resume.extracted_text,
        uploaded_at=resume.uploaded_at,
        analysis=analysis,
    )


@router.get('/my/latest', response_model=ResumeResponse)
def get_latest_resume(db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> Any:
    resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.uploaded_at.desc()).first()
    if not resume:
        raise HTTPException(status_code=404, detail='No resumes found')
    analysis = ResumeService.analyze_text(resume.extracted_text or '')
    return ResumeResponse(
        id=resume.id,
        filename=resume.filename,
        file_path=resume.file_path,
        extracted_text=resume.extracted_text,
        uploaded_at=resume.uploaded_at,
        analysis=analysis,
    )


@router.delete('/{resume_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(resume_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> None:
    resume = db.get(Resume, resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail='Resume not found')

    # Delete file
    try:
        p = Path(resume.file_path)
        if p.exists():
            p.unlink()
    except Exception:
        pass

    db.delete(resume)
    db.commit()
    return None
