import os
from app.services.gemini_service import GeminiService


def test_generate_questions_fallback():
    # Ensure fallback when no API key
    os.environ.pop('GEMINI_API_KEY', None)
    svc = GeminiService()
    out = svc.generate_questions('Acme', 'Backend Engineer', 'resume text', {'skills': ['python']}, n=4)
    assert isinstance(out, list)
    assert len(out) == 4


def test_generate_questions_gemini(monkeypatch):
    os.environ['GEMINI_API_KEY'] = 'test'
    svc = GeminiService()

    sample = '{"questions": [{"category": "PROJECTS", "question": "Explain your AI Interview Coach architecture."}]}'

    monkeypatch.setattr(svc, '_call_generate', lambda prompt: sample)
    svc.enabled = True

    out = svc.generate_questions('Acme', 'Backend', 'resume text', {'projects': ['AI Interview Coach']}, n=1)
    assert out[0]['category'] == 'PROJECTS'
    assert 'AI Interview Coach' in out[0]['text'] or 'architecture' in out[0]['text']
