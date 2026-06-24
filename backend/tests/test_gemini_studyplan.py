import os
from app.services.gemini_service import GeminiService


def test_generate_study_plan_fallback():
    os.environ.pop('GEMINI_API_KEY', None)
    svc = GeminiService()
    out = svc.generate_study_plan({}, ['DBMS', 'DSA'], {})
    assert 'three_day_plan' in out
    assert len(out['three_day_plan']) == 3


def test_generate_study_plan_gemini(monkeypatch):
    os.environ['GEMINI_API_KEY'] = 'test'
    svc = GeminiService()

    sample = '{"three_day_plan": [{"day":1, "task":"Review DBMS"}], "seven_day_plan": [], "thirty_day_plan": []}'
    monkeypatch.setattr(svc, '_call_generate', lambda prompt: sample)
    svc.enabled = True

    out = svc.generate_study_plan({}, ['DBMS'], {})
    assert 'three_day_plan' in out
    assert out['three_day_plan'][0]['task'] == 'Review DBMS'
