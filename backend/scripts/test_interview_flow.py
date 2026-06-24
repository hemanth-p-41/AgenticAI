from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path
from io import BytesIO
import fitz


def make_pdf_bytes(text: str) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    return doc.write()


def test_interview_flow():
    client = TestClient(app)

    # register
    reg = client.post('/auth/register', json={'name': 'Tester', 'email': 'test@example.com', 'password': 'password123'})
    # It's ok if the user already exists from prior test runs (400). Continue to login.
    assert reg.status_code in (200, 201, 400)

    # login
    r = client.post('/auth/login', json={'email': 'test@example.com', 'password': 'password123'})
    assert r.status_code == 200
    token = r.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # upload resume
    pdf_bytes = make_pdf_bytes('Skills: Python, FastAPI\nProjects: Interview Coach')
    files = {'file': ('test.pdf', BytesIO(pdf_bytes), 'application/pdf')}
    up = client.post('/resume/upload', files=files, headers=headers)
    assert up.status_code == 200
    resume = up.json()
    resume_id = resume['id']

    # create interview
    payload = {'company': 'Google', 'role': 'SDE Intern', 'resume_id': resume_id}
    ci = client.post('/interview/create', json=payload, headers=headers)
    assert ci.status_code == 200
    data = ci.json()
    interview_id = data['interview_id']
    assert data['question_count'] == 10

    # get next question
    nq = client.get(f'/interview/{interview_id}/next', headers=headers)
    assert nq.status_code == 200
    q = nq.json()

    # submit answer
    ans = client.post('/interview/answer', json={'question_id': q['question_id'], 'answer': 'This is my answer'}, headers=headers)
    assert ans.status_code == 200

    # progress
    prog = client.get(f'/interview/{interview_id}/progress', headers=headers)
    assert prog.status_code == 200
    p = prog.json()
    assert p['answered'] == 1
    assert p['remaining'] == 9


if __name__ == '__main__':
    test_interview_flow()
    print('Interview flow test passed')
