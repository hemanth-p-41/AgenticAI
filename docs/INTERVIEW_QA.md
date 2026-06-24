# Interview Q&A

## Common interviewer questions
1. What problem does AI Interview Coach solve?
   - It provides personalized interview practice by generating resume-aware questions, evaluating responses, and recommending study topics.

2. Why did you choose FastAPI and Expo React Native?
   - FastAPI provides a lightweight, high-performance backend with modern async support and simple integration for ML and file handling. Expo React Native enables rapid cross-platform mobile/web UI development with a polished experience for interview workflows.

3. How does Gemini integration work in the app?
   - The backend wraps Gemini calls in `backend/app/services/gemini_service.py`. It uses prompt templates to generate interview questions, follow-ups, and answer evaluations, while also supporting fallback deterministic logic to keep the flow stable during local development or API outages.

4. How does the system use resume content?
   - Uploaded PDF resumes are parsed using PyMuPDF. Extracted text is stored and used as context in prompt generation so the questions match the candidates background, skills, and job focus.

5. How do you ensure security and stability?
   - The backend uses JWT authentication, CORS configuration, file validation, and sanitized error responses. Docker support and GitHub Actions CI help enforce consistent builds, linting, testing, and deployment readiness.

6. Can you explain the analytics and study plan flow?
   - Interview responses are stored and scored. The analytics layer identifies weak topics by performance and frequency, then the study plan engine translates those into practice topics and daily tasks for 3-, 7-, and 30-day plans.

7. What was the hardest part of this project?
   - Designing a robust interview flow with AI-generated prompts, answer evaluation, and persistence while keeping the app deterministic enough to test locally. Balancing LLM flexibility with reproducible fallback behavior was the main challenge.

## Technical deep-dive questions
1. Describe how you modeled interview sessions in the database.
   - Interview sessions are backed by tables for interviews, questions, responses, and analytics metadata. Each session persists the user, company, question sequence, and response evaluations to enable longitudinal performance tracking.

2. How would you improve the project for production?
   - Switch SQLite to PostgreSQL, use cloud file storage, add async task processing for LLM calls, improve prompt caching, and add end-to-end test coverage for the frontend.

3. How did you handle prompt engineering for Gemini?
   - I used structured prompts with explicit instructions, resume excerpts, and role definitions to generate relevant question sets and evaluation criteria. I also persisted prompt templates in code so they are easy to tune.

4. How do you keep the backend testable without Gemini API access?
   - I built deterministic fallback routines that mimic LLM outputs with consistent sample questions and scoring rules. This lets the interview flow execute in CI and local environments even when API credentials are missing.

5. What libraries were critical to the backend?
   - FastAPI, SQLAlchemy, Alembic, PyMuPDF, Pydantic, and `google-generativeai` for Gemini. For dev tooling, black, isort, flake8, and pytest ensured code quality.
