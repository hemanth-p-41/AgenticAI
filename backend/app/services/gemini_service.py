import os
import logging
import time
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai  # type: ignore
except Exception:  # pragma: no cover - import may fail in test env
    genai = None

from app.utils.json_utils import safe_json_parser


class GeminiService:
    """Centralized Gemini service wrapper using `google-generativeai`.

    When `GEMINI_API_KEY` is unset the service falls back to deterministic
    generators to preserve offline testing and reliability.
    """

    def __init__(self, retries: int = 3, timeout: float = 10.0):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.enabled = bool(self.api_key) and genai is not None
        self.retries = retries
        self.timeout = timeout

        if self.enabled:
            try:
                genai.configure(api_key=self.api_key)
            except Exception:
                logger.exception("Failed to configure Gemini client; disabling")
                self.enabled = False

    def _call_generate(self, prompt: str, model: str = "gemini-2.5-flash") -> str:
        """Call the Gemini SDK (wrapped) and return raw text output.

        This method isolates SDK usage so it can be monkeypatched in tests.
        """
        if not self.enabled:
            raise RuntimeError("Gemini not enabled")

        # Basic retry loop
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.retries + 1):
            try:
                # The SDK may accept a single string or a messages list; keep it
                # generic and rely on SDK's generate function.
                resp = genai.generate(model=model, prompt=prompt)
                # Try to extract textual output from common response shapes
                if hasattr(resp, 'text'):
                    return resp.text
                if hasattr(resp, 'result'):
                    return str(resp.result)
                if isinstance(resp, str):
                    return resp
                # fallback to string coercion
                return str(resp)
            except Exception as e:
                last_exc = e
                logger.warning("Gemini generate attempt %s failed: %s", attempt, e)
                time.sleep(0.5 * attempt)

        raise last_exc or RuntimeError("Gemini generate failed")

    def generate_questions(self, company: str, role: str, resume_text: str, analysis: Dict, n: int = 10) -> List[Dict[str, Any]]:
        """Generate structured interview questions as strict JSON.

        Returns list of {"category":..., "question":...}. Falls back to deterministic
        generator on failure or when Gemini is not enabled.
        """
        if not self.enabled:
            return self._fallback_generate_questions(company, role, resume_text, analysis, n)

        prompt = (
            "You are an interview generator. Produce strict JSON with a top-level 'questions' array. "
            "Each question must be an object with 'category' and 'question'."
            f"\ncompany: {company}\nrole: {role}\nresume_excerpt: {resume_text[:1000]}\nanalysis: {analysis}\ncount: {n}\n"
            "Return only valid JSON."
        )

        try:
            raw = self._call_generate(prompt)
            data = safe_json_parser(raw)
            questions = data.get('questions') if isinstance(data, dict) else None
            if not questions or not isinstance(questions, list):
                raise ValueError('Invalid questions payload')
            # normalize keys
            out = []
            for q in questions:
                out.append({'category': q.get('category', 'GENERAL'), 'text': q.get('question') or q.get('text')})
            return out
        except Exception:
            logger.exception('Gemini questions generation failed; using fallback')
            return self._fallback_generate_questions(company, role, resume_text, analysis, n)

    def generate_followup_question(self, question_text: str, answer_text: str, context: Dict = None) -> str:
        if not self.enabled:
            return f"Can you explain how you implemented or tested: {question_text.split('?')[0]}?"

        prompt = (
            "Given the previous question and the candidate's answer, generate a single concise follow-up question."
            f"\nprevious_question: {question_text}\nanswer: {answer_text}\ncontext: {context or {}}\n"
            "Return only a JSON object: {\"followup_question\": \"...\"}."
        )

        try:
            raw = self._call_generate(prompt)
            data = safe_json_parser(raw)
            return data.get('followup_question') or str(data)
        except Exception:
            logger.exception('Gemini follow-up failed; using simple heuristic')
            return f"Can you elaborate on: {question_text.split('?')[0]}?"

    def evaluate_answer(self, question_text: str, answer_text: str, resume_text: str) -> Dict[str, Any]:
        if not self.enabled:
            # Existing deterministic evaluation is handled elsewhere; provide fallback
            return {
                'score': 5,
                'strengths': [],
                'weaknesses': [],
                'suggestions': [],
                'ideal_answer': ''
            }

        prompt = (
            "Evaluate the candidate's answer to the question. Return strict JSON with keys: score (0-10), strengths, weaknesses, suggestions, ideal_answer."
            f"\nquestion: {question_text}\nanswer: {answer_text}\nresume: {resume_text[:2000]}\n"
        )

        try:
            raw = self._call_generate(prompt)
            data = safe_json_parser(raw)
            # Validate minimal fields
            score = int(data.get('score', 0)) if isinstance(data, dict) else 0
            return {
                'score': max(0, min(10, score)),
                'strengths': data.get('strengths', []) if isinstance(data, dict) else [],
                'weaknesses': data.get('weaknesses', []) if isinstance(data, dict) else [],
                'suggestions': data.get('suggestions', []) if isinstance(data, dict) else [],
                'ideal_answer': data.get('ideal_answer', '') if isinstance(data, dict) else ''
            }
        except Exception:
            logger.exception('Gemini evaluation failed; using fallback')
            return {
                'score': 5,
                'strengths': [],
                'weaknesses': [],
                'suggestions': [],
                'ideal_answer': ''
            }

    def generate_study_plan(self, analytics: Dict, weak_categories: List[str], trends: Dict) -> Dict[str, Any]:
        if not self.enabled:
            # Simple deterministic plan
            return {
                'three_day_plan': [{'day': i+1, 'task': f"Review {weak_categories[i%len(weak_categories)] if weak_categories else 'fundamentals'}"} for i in range(3)],
                'seven_day_plan': [{'day': i+1, 'task': 'Practice problems and review notes'} for i in range(7)],
                'thirty_day_plan': [{'day': i+1, 'task': 'Deep dive project or course'} for i in range(30)]
            }

        prompt = (
            "Produce a study plan JSON with keys three_day_plan, seven_day_plan, thirty_day_plan. Each is an array of {day:int, task:str}."
            f"\nanalytics: {analytics}\nweak_categories: {weak_categories}\ntrends: {trends}\n"
        )

        try:
            raw = self._call_generate(prompt)
            data = safe_json_parser(raw)
            return data
        except Exception:
            logger.exception('Gemini study plan failed; using fallback')
            return self.generate_study_plan({}, weak_categories or [], {})

    def _fallback_generate_questions(self, company: str, role: str, resume_text: str, analysis: Dict, n: int) -> List[Dict]:
        categories = ['DSA', 'OOP', 'DBMS', 'OS', 'Projects', 'Behavioral']
        skills = analysis.get('skills', []) if analysis else []
        projects = analysis.get('projects', []) if analysis else []

        out = []
        for i in range(n):
            cat = categories[i % len(categories)]
            if cat == 'Projects' and projects:
                proj = projects[i % len(projects)]
                text = f"Walk me through the project '{proj}' and your technical contributions."
            elif cat == 'Behavioral':
                text = f"Tell me about a time you faced a difficult bug or design decision and how you resolved it."
            elif cat == 'DSA':
                text = f"Describe an efficient algorithm to solve a real-world problem related to {role} at {company}. Provide complexity analysis."
            elif cat == 'OOP':
                text = f"Design a class structure for a simplified version of a system you'd build as a {role}. Discuss OOP principles."
            elif cat == 'DBMS':
                text = f"How would you design the database schema for storing resumes and interview sessions for scale?"
            elif cat == 'OS':
                text = f"Explain how process scheduling or memory management could affect a high-throughput service."
            else:
                text = f"Explain the concept of {skills[0] if skills else 'scalability'} and how you'd apply it in a production system."

            out.append({'text': text, 'category': cat})

        return out
