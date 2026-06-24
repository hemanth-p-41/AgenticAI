# STAR Stories

## Story 1: Building Reliable AI Interview Feedback
- Situation: I was building an interview preparation application that relied on Gemini for question generation and answer evaluation.
- Task: I needed the system to remain testable and stable even when API access was unavailable or when credentials were missing in local development.
- Action: I created a dedicated `GeminiService` layer in `backend/app/services/gemini_service.py` that abstracts prompt invocation and includes deterministic fallback logic. This allowed API calls to be swapped with consistent sample outputs during development and CI.
- Result: The app became reliable for local testing and CI workflows while still supporting live Gemini responses in production. This improved developer confidence and reduced intermittent failures due to API availability.

## Story 2: Designing Resume-Aware Question Generation
- Situation: Generic interview practice tools were not helping candidates prepare with questions relevant to their skills and experience.
- Task: I wanted to produce interview questions that reflected a candidates resume and target company.
- Action: I added PDF resume upload and text extraction using PyMuPDF. I then fed the parsed resume content into prompt templates used by the Gemini service, enabling questions to include resume-specific context.
- Result: The platform can generate much more relevant practice questions, helping candidates focus on their actual strengths and role fit.

## Story 3: Shipping Production Readiness with CI/CD
- Situation: The project needed a polished delivery path beyond prototype code.
- Task: I needed to ensure the backend and frontend were quality-controlled, linted, tested, and deployable.
- Action: I created GitHub Actions workflows for backend and frontend CI, added Docker deployment artifacts, and documented production readiness in `docs/PRODUCTION_CHECKLIST.md` and `docs/DEPLOY_DOCKER.md`.
- Result: The project now has a quality gate for code changes and a reproducible deployment path, making it easier to present as a professional portfolio project.
