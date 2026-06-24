import os
from app.services.gemini_service import GeminiService


def test_evaluate_answer_fallback():
    os.environ.pop('GEMINI_API_KEY', None)
    svc = GeminiService()
    out = svc.evaluate_answer('Q', 'A', 'resume')
    assert isinstance(out, dict)
    assert 'score' in out


def test_evaluate_answer_gemini(monkeypatch):
    os.environ['GEMINI_API_KEY'] = 'test'
    svc = GeminiService()

    sample = '{"score": 8, "strengths": ["clarity"], "weaknesses": ["detail"], "suggestions": ["add tests"], "ideal_answer": "..."}'
    monkeypatch.setattr(svc, '_call_generate', lambda prompt: sample)
    svc.enabled = True

    out = svc.evaluate_answer('Explain X', 'I did X', 'resume')
    assert out['score'] == 8
    assert 'clarity' in out['strengths']
