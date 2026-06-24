"""In-process tests for auth endpoints using FastAPI TestClient."""
from app.main import app
from fastapi.testclient import TestClient


def run() -> None:
    client = TestClient(app)
    email = 'inproc_user@example.com'
    password = 'password123'
    name = 'InProc User'

    print('Registering...')
    r = client.post('/auth/register', json={'name': name, 'email': email, 'password': password})
    print('register', r.status_code, r.text)

    print('Logging in...')
    r = client.post('/auth/login', json={'email': email, 'password': password})
    print('login', r.status_code, r.text)
    if r.status_code != 200:
        return
    token = r.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    print('Getting /auth/me...')
    r = client.get('/auth/me', headers=headers)
    print('me', r.status_code, r.text)


if __name__ == '__main__':
    run()
