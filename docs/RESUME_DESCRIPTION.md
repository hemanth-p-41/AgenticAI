# Resume-ready Project Description

Two-line summary
- AI Interview Coach: a FastAPI backend and Expo React Native frontend that generates company-specific interview questions from uploaded resumes, evaluates answers using Gemini, and produces personalized study plans.

Five-line detailed description
- Implements secure registration and JWT authentication, PDF resume upload and parsing (PyMuPDF), and a deterministic interview engine.
- Integrates Gemini (google-generativeai) to generate tailored questions, follow-ups, and to evaluate answers (with deterministic fallbacks).
- Stores structured interview data and analytics for weakness detection and study plan generation.
- Frontend: Expo React Native TypeScript app with navigation, auth context, and API service wrappers for seamless UX.
- Delivery: Docker-enabled backend, docs, tests, and deploy guidance for demos and portfolio showcase.

Technologies: FastAPI, SQLAlchemy, PyMuPDF, google-generativeai, Expo React Native, TypeScript, Docker

Key achievements
- End-to-end interview flow with LLM integration and deterministic offline fallbacks.
- Production-focused deploy artifacts (Docker, docker-compose) and documentation for reviewers.
