# Architecture

Backend
- FastAPI app in `backend/app`.
- Services: resume parsing, Gemini integration, interview engine, evaluation, analytics, study-plan.
- SQLite (dev) / PostgreSQL (prod) via `DATABASE_URL`.

Frontend
- Expo React Native TypeScript app in `frontend/`.
- Screens for auth, resume, interview, evaluation, analytics, study plans.

Gemini Workflow
- `app/services/gemini_service.py` encapsulates calls; falls back to deterministic logic when `GEMINI_API_KEY` absent.
