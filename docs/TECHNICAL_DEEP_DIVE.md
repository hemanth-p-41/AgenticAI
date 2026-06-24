# Technical Deep Dive

## System Overview
AI Interview Coach is built as a modular full-stack application. The backend is a FastAPI service that handles auth, resume upload, interview session management, question generation, answer scoring, analytics, and study-plan generation. The frontend is an Expo React Native app that consumes these APIs and provides an interactive practice experience.

## Backend Architecture
- `backend/app/main.py`: FastAPI app configuration, middleware, CORS, and startup/shutdown lifecycle.
- `backend/app/models/`: SQLAlchemy ORM models define users, resumes, interviews, questions, responses, analytics, and study plans.
- `backend/app/schemas/`: Pydantic schemas validate request and response structures for safe API contracts.
- `backend/app/services/gemini_service.py`: Encapsulates Gemini prompt orchestration with fallback logic.
- `backend/app/utils/json_utils.py`: Handles robust JSON parsing for LLM outputs and markdown-safe deserialization.
- `backend/app/utils/logger.py`: Configures rotating file and console logging for diagnostics.

## LLM Integration
- Gemini is integrated through `google-generativeai` with environment-driven credentials.
- The backend uses carefully designed prompts to generate company-specific questions and evaluate answers against resume content, role expectations, and performance criteria.
- Deterministic fallback paths simulate question generation and evaluation when Gemini credentials are absent, ensuring the app can still function in local and CI environments.

## Resume Processing
- PDF resumes are uploaded and stored as files, then parsed using PyMuPDF.
- Extracted text is persisted and used within LLM prompts to ground question generation.
- This enables the system to reflect resume-specific experiences and skills in its interview questions.

## Interview Flow
- Users create interview sessions by selecting a company or target role.
- The system generates an initial question set and optional follow-up prompts for focus or detail.
- Responses are submitted and scored, with results saved to the backend.
- Analytics aggregate scores and performance trends across sessions.

## Analytics and Study Plans
- The analytics layer tracks topic trends, average scores, and identified weakness areas.
- Study plans are generated based on weak topics and session frequency, organized into 3-, 7-, and 30-day plans for consistent review.
- This helps users remediate gaps with prioritized practice topics.

## Deployment and Production Readiness
- Docker support exists for containerized backend deployments.
- GitHub Actions CI enforces linting, formatting, and unit tests on backend and frontend changes.
- Environment configuration supports separate dev and prod settings, including database, AI credentials, and CORS origins.

## Future Improvements
- Add async worker queues for LLM calls to improve scale and user experience.
- Upgrade the database to PostgreSQL and add migration support for multi-tenant data.
- Add a web dashboard for deeper analytics and aggregated interview performance.
- Add richer prompt caching, retry handling, and rate-limit-aware Gemini calls.
- Extend the frontend with interview coaching tips, timed mock interviews, and audio recording.
