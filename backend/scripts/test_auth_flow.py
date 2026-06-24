"""Test script for authentication endpoints: register, login, me."""
import time
import httpx
import os

BASE = os.getenv('BASE_URL', 'http://127.0.0.1:8000')


def run() -> None:
    client = httpx.Client()
    # unique email to avoid collisions
    email = 'test_user@example.com'
    password = 'password123'
    name = 'Test User'

    print('Registering user...')
    r = client.post(f'{BASE}/auth/register', json={'name': name, 'email': email, 'password': password})
    print('Register status:', r.status_code)
    print(r.text)

    print('Logging in...')
    r = client.post(f'{BASE}/auth/login', json={'email': email, 'password': password})
    print('Login status:', r.status_code)
    print(r.text)
    if r.status_code != 200:
        return
    token = r.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    print('Accessing /auth/me...')
    r = client.get(f'{BASE}/auth/me', headers=headers)
    print('Me status:', r.status_code)
    print(r.text)


if __name__ == '__main__':
    # small delay for server startup if needed
    time.sleep(1)
    run()
