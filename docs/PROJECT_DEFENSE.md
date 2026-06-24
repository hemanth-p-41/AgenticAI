# Project Defense

## Why this project is valuable
- It addresses a real candidate pain point: interview practice that is generic instead of resume-specific.
- It combines AI with practical user workflows: resume upload, interview sessions, feedback, and study guidance.
- It shows end-to-end product thinking with backend APIs, frontend UX, deployment, and documentation.

## What I learned
- How to integrate generative AI into a real application while keeping the flow testable and robust.
- How to design clean API contracts and database models for multi-step interview experiences.
- How to build cross-platform UI with Expo React Native and connect it to a backend service.
- How to package a project with Docker and CI to make it presentable for hiring managers.

## Risks and mitigation
- Gemini API availability: mitigated by fallback logic and local deterministic behavior.
- Data persistence: currently SQLite for development; production should use PostgreSQL or managed DB.
- File storage: PDF files are stored locally now; production should use secure object storage like S3.
- Scalability: current architecture works for MVP; future improvements include async LLM jobs and prompt caching.

## What I would improve next
- Add a web dashboard for recruiters and deeper analytics.
- Build asynchronous background jobs for Gemini calls and resume processing.
- Add full end-to-end tests with frontend automation.
- Replace SQLite with PostgreSQL and add cloud storage for resumes.
- Expand the AI coaching engine with timed mock interviews and personalized feedback templates.

## Defense talking points
- "The core value is not just AI generation, but actionable interview preparation guided by a candidate's resume."
- "I kept the architecture modular so the Gemini layer and fallback logic are separate from the rest of the backend."
- "Production readiness was a priority: Docker, CI/CD workflows, documentation, and clean environment configuration were all part of the delivery."
- "This project is a strong portfolio piece because it blends backend, frontend, ML integration, and devops practices."
