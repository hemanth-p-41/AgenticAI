"""In-process tests for resume upload and retrieval using TestClient."""
from app.main import app
from fastapi.testclient import TestClient
import io
import fitz


def make_pdf_bytes(text: str = "Hello PDF") -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    buf = doc.write()  # returns bytes
    return buf


def run() -> None:
    client = TestClient(app)
    # Reuse or create a test user via auth endpoints
    email = 'resume_user@example.com'
    password = 'password123'
    name = 'Resume User'

    # Ensure user exists
    client.post('/auth/register', json={'name': name, 'email': email, 'password': password})
    r = client.post('/auth/login', json={'email': email, 'password': password})
    if r.status_code != 200:
        print('Login failed', r.status_code, r.text)
        return
    token = r.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # Create a PDF bytes
    pdf_bytes = make_pdf_bytes('Skills: Python, FastAPI\nProjects: AI Interview Coach')

    files = {'file': ('test.pdf', pdf_bytes, 'application/pdf')}
    r = client.post('/resume/upload', headers=headers, files=files)
    print('upload', r.status_code, r.text)
    if r.status_code != 200 and r.status_code != 201:
        return
    resume_id = r.json()['id']

    r = client.get(f'/resume/{resume_id}', headers=headers)
    print('get', r.status_code, r.text)


if __name__ == '__main__':
    run()
