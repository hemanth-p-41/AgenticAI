# AI Interview Coach

[![Backend CI](https://github.com/<OWNER>/<REPO>/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/<OWNER>/<REPO>/actions/workflows/backend-ci.yml)
[![Frontend CI](https://github.com/<OWNER>/<REPO>/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/<OWNER>/<REPO>/actions/workflows/frontend-ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.14+-blue)](https://www.python.org/)

> AI Interview Coach is a full-stack interview preparation platform that turns resumes into personalized practice sessions, automated feedback, analytics, and study plans.

## 🚀 Project Banner

**AI Interview Coach** combines a production-ready FastAPI backend, Expo React Native frontend, and Gemini-powered AI orchestration to enable resume-aware interview practice.

- Resume upload and parsing using PyMuPDF
- Dynamic question generation and answer evaluation
- Analytics-driven weakness detection and study plans
- Docker-enabled deployment and GitHub Actions CI/CD

## ✨ Features

- User authentication and secure resume upload
- PDF resume text extraction and resume-aware question generation
- Gemini-powered interview prompt generation, follow-ups, and answer scoring
- Interview session persistence with analytics and performance tracking
- Adaptive 3/7/30-day study plan generation
- Docker container support and CI/CD automation

## 🏗 Architecture

```mermaid
flowchart LR
    A[Frontend (Expo React Native)] -->|API Requests| B[FastAPI Backend]
    B --> C[Authentication / JWT]
    B --> D[Resume Service / PyMuPDF]
    B --> E[Interview Engine]
    E --> F[Gemini Service / LLM prompts]
    B --> G[Database (SQLite / PostgreSQL)]
    B --> H[Analytics + Study Plan Engine]
    H --> A
    subgraph Storage
      G
    end
    subgraph AI
      F
    end
```

## 🧰 Tech Stack

- Backend: FastAPI, SQLAlchemy, Alembic
- AI: Google Gemini via `google-generativeai`, deterministic fallback support
- Resume parsing: PyMuPDF
- Frontend: Expo React Native, TypeScript
- Deployment: Docker, GitHub Actions
- Testing / Quality: pytest, black, isort, flake8

## 🖼 Screenshots

> Replace these placeholders with actual app screenshots once available.

- `docs/screenshots/landing.png`
- `docs/screenshots/interview-session.png`
- `docs/screenshots/analytics-dashboard.png`
- `docs/screenshots/study-plan.png`

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/<OWNER>/<REPO>.git
cd "Agentic AI"
```

### 2. Backend setup

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
cp .env.example .env
```

Configure `.env` with your database and Gemini credentials.

### 3. Frontend setup

```bash
cd ../frontend
npm install
```

### 4. Run locally

```bash
cd ../backend
source .venv/Scripts/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
cd ../frontend
npm start
```

## 📚 API Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [CI/CD](docs/CI_CD.md)
- [Docker Deployment](docs/DEPLOY_DOCKER.md)
- [Production Checklist](docs/PRODUCTION_CHECKLIST.md)
- [Interview Prep Guide](docs/INTERVIEW_PREP.md)
- [API Reference](docs/API_REFERENCE.md)

## 🚢 Deployment

### Docker Compose

```bash
docker-compose up --build
```

### Production notes

- Use PostgreSQL or managed database for production
- Store uploaded resumes in secure object storage (S3, Azure Blob, etc.)
- Secure environment variables and Gemini API keys
- Run migrations via Alembic before startup

## 🧪 CI / CD

This project includes GitHub Actions workflows for backend and frontend validation.

- `backend/.github/workflows/backend-ci.yml`
- `frontend/.github/workflows/frontend-ci.yml`

## 🌱 Roadmap

- [ ] Add full end-to-end frontend automated tests
- [ ] Upgrade database support to PostgreSQL
- [ ] Add secure cloud storage for resume files
- [ ] Introduce async job queue for Gemini requests
- [ ] Build a recruiter dashboard and richer analytics
- [ ] Add voice-enabled mock interview support

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/name`
3. Commit your changes: `git commit -m "Add feature"`
4. Push to your branch: `git push origin feature/name`
5. Open a pull request

Please follow existing code style, update tests if applicable, and keep commits focused.

## 📝 License

This project is licensed under the MIT License. See `LICENSE` for details.

## 📄 Notes

Update the badge URLs from `<OWNER>/<REPO>` to your repository path once you publish the project.
