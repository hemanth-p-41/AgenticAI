# CI / CD Documentation

This project includes GitHub Actions workflows for backend and frontend validation.

Workflows

- `.github/workflows/backend-ci.yml` - runs on push/pull_request to `backend/**`:
  - installs Python dependencies
  - runs code format and lint checks (black, isort, flake8)
  - runs pytest with coverage
  - runs pip-audit
  - applies alembic migrations to `dev.db` for verification
  - attempts a Docker build of the backend image

- `.github/workflows/frontend-ci.yml` - runs on push/pull_request to `frontend/**`:
  - installs Node deps
  - TypeScript check
  - lints with ESLint
  - runs `npm run build` if present

Local testing

- Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install black isort flake8 pytest pytest-cov pip-audit
black . --check
isort . --check-only
flake8 .
pytest --cov=app
pip-audit
alembic upgrade head
```

- Frontend:

```bash
cd frontend
npm ci
npx tsc --noEmit
npx eslint .
npm run build # optional
```

Deployment

- Use Docker Compose or CI to build and push images to a registry, then deploy to your hosting platform.

*** End ***
