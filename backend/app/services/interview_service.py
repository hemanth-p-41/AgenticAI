from typing import Optional
from sqlalchemy.orm import Session
from app.models.interview import Interview
from app.models.question import Question
from app.models.response import Response
from app.services.gemini_service import GeminiService
from app.services.resume_service import ResumeService


class InterviewService:
    def __init__(self, db: Session):
        self.db = db
        self.gemini = GeminiService()

    def create_interview(self, user, company: str, role: str, resume_id: int) -> Interview:
        # verify resume ownership
        resume = self.db.get(type(user).resumes.property.mapper.class_, resume_id)
        if not resume or resume.user_id != user.id:
            raise ValueError('Invalid resume or not owned by user')

        # prepare analysis and text
        text = resume.extracted_text or ''
        analysis = ResumeService.analyze_text(text)

        interview = Interview(user_id=user.id, company=company, role=role)
        self.db.add(interview)
        self.db.commit()
        self.db.refresh(interview)

        # generate questions via GeminiService (or fallback)
        qlist = self.gemini.generate_questions(company, role, text, analysis, n=10)

        for q in qlist:
            question = Question(interview_id=interview.id, text=q.get('text'), category=q.get('category'))
            self.db.add(question)

        self.db.commit()

        return interview

    def get_next_question(self, interview_id: int) -> Optional[Question]:
        # return next unanswered question (without responses)
        q = (
            self.db.query(Question)
            .filter(Question.interview_id == interview_id)
            .outerjoin(Response, Response.question_id == Question.id)
            .group_by(Question.id)
            .having(~(Response.id.isnot(None)))
        )
        # The above having is complex; simpler: query questions and pick first with no responses
        qs = self.db.query(Question).filter(Question.interview_id == interview_id).order_by(Question.id).all()
        for question in qs:
            if not question.responses:
                return question
        return None

    def submit_answer(self, user, question_id: int, answer_text: str) -> Response:
        question = self.db.get(Question, question_id)
        if not question:
            raise ValueError('Question not found')
        interview = self.db.get(Interview, question.interview_id)
        if interview.user_id != user.id:
            raise ValueError('Not authorized for this interview')

        resp = Response(question_id=question.id, interview_id=interview.id, user_id=user.id, answer_text=answer_text)
        self.db.add(resp)
        self.db.commit()
        self.db.refresh(resp)
        return resp

    def get_progress(self, interview_id: int) -> dict:
        total = self.db.query(Question).filter(Question.interview_id == interview_id).count()
        answered = (
            self.db.query(Response).filter(Response.interview_id == interview_id).count()
        )
        remaining = max(total - answered, 0)
        pct = int((answered / total) * 100) if total > 0 else 0
        return {'answered': answered, 'remaining': remaining, 'completion_percentage': pct}
