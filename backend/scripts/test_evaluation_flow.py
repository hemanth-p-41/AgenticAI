from fastapi.testclient import TestClient
from app.main import app
from io import BytesIO
import fitz


def make_pdf_bytes(text: str) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    return doc.write()


def test_evaluation_flow():
    client = TestClient(app)

    # register/login
    client.post('/auth/register', json={'name': 'EvalUser', 'email': 'eval@example.com', 'password': 'password123'})
    r = client.post('/auth/login', json={'email': 'eval@example.com', 'password': 'password123'})
    token = r.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # upload resume
    pdf_bytes = make_pdf_bytes('Skills: Python, FastAPI\nProjects: Evaluation Engine')
    files = {'file': ('test.pdf', BytesIO(pdf_bytes), 'application/pdf')}
    up = client.post('/resume/upload', files=files, headers=headers)
    resume_id = up.json()['id']

    # create interview
    ci = client.post('/interview/create', json={'company': 'Acme', 'role': 'Backend', 'resume_id': resume_id}, headers=headers)
    interview_id = ci.json()['interview_id']

    # get next question and submit answer
    nq = client.get(f'/interview/{interview_id}/next', headers=headers)
    q = nq.json()
    ans = client.post('/interview/answer', json={'question_id': q['question_id'], 'answer': 'This is an evaluation test answer that references Python and FastAPI.'}, headers=headers)
    assert ans.status_code == 200

    # evaluate single answer
    ev = client.post('/evaluation', json={'question_id': q['question_id'], 'answer': 'This is an evaluation test answer that references Python and FastAPI.'}, headers=headers)
    assert ev.status_code == 200
    data = ev.json()
    assert 'score' in data

    # bulk evaluate interview
    be = client.post(f'/evaluation/interview/{interview_id}', headers=headers)
    assert be.status_code == 200
    bdata = be.json()
    assert 'average_score' in bdata

    # summary
    s = client.get(f'/evaluation/interview/{interview_id}', headers=headers)
    assert s.status_code == 200
    sj = s.json()
    assert 'average_score' in sj


if __name__ == '__main__':
    test_evaluation_flow()
    print('Evaluation flow test passed')
