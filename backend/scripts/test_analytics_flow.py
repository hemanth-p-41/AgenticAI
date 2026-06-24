from fastapi.testclient import TestClient
from app.main import app
from io import BytesIO
import fitz


def make_pdf_bytes(text: str) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    return doc.write()


def test_analytics_and_studyplan_flow():
    client = TestClient(app)
    # register/login
    client.post('/auth/register', json={'name': 'AnaUser', 'email': 'ana@example.com', 'password': 'password123'})
    r = client.post('/auth/login', json={'email': 'ana@example.com', 'password': 'password123'})
    token = r.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # upload resume
    pdf_bytes = make_pdf_bytes('Skills: Python, FastAPI\nProjects: Analytics')
    files = {'file': ('test.pdf', BytesIO(pdf_bytes), 'application/pdf')}
    up = client.post('/resume/upload', files=files, headers=headers)
    resume_id = up.json()['id']

    # create interview and answer one question and evaluate
    ci = client.post('/interview/create', json={'company': 'X', 'role': 'Y', 'resume_id': resume_id}, headers=headers)
    interview_id = ci.json()['interview_id']
    nq = client.get(f'/interview/{interview_id}/next', headers=headers).json()
    client.post('/interview/answer', json={'question_id': nq['question_id'], 'answer': 'Answer referencing Python'}, headers=headers)
    client.post('/evaluation', json={'question_id': nq['question_id'], 'answer': 'Answer referencing Python'}, headers=headers)

    # analytics
    ana = client.get('/analytics/me', headers=headers)
    assert ana.status_code == 200
    tr = client.get('/analytics/trends', headers=headers)
    assert tr.status_code == 200
    wk = client.get('/analytics/weaknesses', headers=headers)
    assert wk.status_code == 200

    # study plan
    sp = client.get('/study-plan/me', headers=headers)
    assert sp.status_code == 200
    print('Analytics and study plan test passed')


if __name__ == '__main__':
    test_analytics_and_studyplan_flow()
