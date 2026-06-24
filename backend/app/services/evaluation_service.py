from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.response import Response
from app.models.question import Question
from app.models.interview import Interview
from app.services.gemini_service import GeminiService
from app.services.resume_service import ResumeService


class EvaluationService:
    def __init__(self, db: Session):
        self.db = db
        self.gemini = GeminiService()

    def evaluate_answer(self, question_id: int, answer_text: str, user) -> Dict[str, Any]:
        question = self.db.get(Question, question_id)
        if not question:
            raise ValueError('Question not found')

        interview = self.db.get(Interview, question.interview_id)
        if interview.user_id != user.id:
            raise ValueError('Not authorized')

        # retrieve resume via interview -> we stored no direct resume id on interview, so attempt to find
        # the latest resume for the user as a proxy
        # In future, store resume_id on Interview model.
        resume_text = ''
        analysis = {}
        from app.models.resume import Resume
        res = (
            self.db.query(Resume).filter(Resume.user_id == user.id).order_by(Resume.uploaded_at.desc()).first()
        )
        if res:
            resume_text = res.extracted_text or ''
            analysis = ResumeService.analyze_text(resume_text)

        if self.gemini.enabled:
            # Placeholder: real Gemini evaluation integration should use build_evaluation_prompt
            raise NotImplementedError('Gemini evaluation not implemented; set GEMINI_API_KEY to enable')

        # Fallback deterministic evaluation
        eval_result = self._fallback_evaluate(question.text, answer_text, analysis)

        # store into Response.evaluation JSON
        # find the response row corresponding to this question and user
        resp = (
            self.db.query(Response)
            .filter(Response.question_id == question_id, Response.user_id == user.id)
            .order_by(Response.created_at.desc())
            .first()
        )
        if not resp:
            # create a new response record if none exists
            resp = Response(question_id=question_id, interview_id=interview.id, user_id=user.id, answer_text=answer_text)
            self.db.add(resp)

        resp.evaluation = eval_result
        self.db.add(resp)
        self.db.commit()
        self.db.refresh(resp)

        return eval_result

    def _fallback_evaluate(self, question_text: str, answer_text: str, analysis: Dict) -> Dict[str, Any]:
        # Score heuristics: base on length and presence of keywords from analysis.skills
        base = min(max(len(answer_text.split()) // 10, 3), 9)
        skills = analysis.get('skills', [])
        bonus = 1 if skills and any(s.lower() in answer_text.lower() for s in skills[:3]) else 0
        score = min(base + bonus, 10)

        strengths = []
        weaknesses = []
        suggestions = []

        if len(answer_text) > 50:
            strengths.append('Provides detailed explanation')
        else:
            weaknesses.append('Answer is brief; expand with examples')

        if skills and any(s.lower() in answer_text.lower() for s in skills):
            strengths.append('References relevant skills')
        else:
            suggestions.append('Include explicit references to resume skills')

        ideal = f"An ideal answer would cover the approach, complexity, trade-offs, and an example."

        category = question_text.split()[0].upper() if question_text else 'PROJECTS'

        return {
            'score': score,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'suggestions': suggestions,
            'ideal_answer': ideal,
            'category': category,
        }

    def bulk_evaluate_interview(self, interview_id: int, user) -> Dict[str, Any]:
        # find all responses in interview without evaluation
        resps = (
            self.db.query(Response)
            .filter(Response.interview_id == interview_id, Response.evaluation == None)
            .all()
        )
        evaluated = 0
        total_score = 0
        for r in resps:
            ev = self.evaluate_answer(r.question_id, r.answer_text, user)
            evaluated += 1
            total_score += ev.get('score', 0)

        avg = (total_score / evaluated) if evaluated > 0 else 0.0
        return {'average_score': avg, 'evaluated_questions': evaluated}

    def interview_summary(self, interview_id: int) -> Dict[str, Any]:
        # aggregate evaluations for interview
        resps = self.db.query(Response).filter(Response.interview_id == interview_id, Response.evaluation != None).all()
        if not resps:
            return {'average_score': 0.0, 'strongest_area': None, 'weakest_area': None, 'question_breakdown': []}

        # compute average and per-category
        total = 0
        per_cat = {}
        breakdown = []
        for r in resps:
            ev = r.evaluation or {}
            score = ev.get('score', 0)
            cat = ev.get('category', 'UNKNOWN')
            total += score
            per_cat.setdefault(cat, []).append(score)
            breakdown.append({'question_id': r.question_id, 'score': score, 'category': cat, 'strengths': ev.get('strengths', []), 'weaknesses': ev.get('weaknesses', []), 'suggestions': ev.get('suggestions', [])})

        avg = total / len(resps)
        # strongest and weakest by average score
        cat_avgs = {k: sum(v) / len(v) for k, v in per_cat.items()}
        strongest = max(cat_avgs.items(), key=lambda kv: kv[1])[0] if cat_avgs else None
        weakest = min(cat_avgs.items(), key=lambda kv: kv[1])[0] if cat_avgs else None
        return {'average_score': avg, 'strongest_area': strongest, 'weakest_area': weakest, 'question_breakdown': breakdown}
