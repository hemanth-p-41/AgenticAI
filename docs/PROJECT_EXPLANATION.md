# Project Explanation

## Problem Statement
Job seekers need realistic, personalized interview practice that reflects their resume, target company, and technical profile. Existing tools often provide generic questions, lack answer feedback, and do not generate tailored study plans.

## Solution
AI Interview Coach solves this by combining resume parsing, targeted question generation, answer evaluation, analytics, and tailored study plans in one platform. Users upload a resume, get resume-aware interview questions, answer them in-app, and receive automated feedback plus suggested areas to improve.

## Architecture
The system uses a FastAPI backend for business logic and a React Native Expo frontend for cross-platform access. The backend persists users, resumes, interviews, questions, responses, analytics, and study plans in a SQL-based database. Gemini is integrated through a dedicated service layer for question generation and evaluation, with deterministic fallbacks to ensure reliability without API access.

## Features
- JWT-based authentication
- PDF resume upload and extraction with PyMuPDF
- Company-specific interview creation
- Gemini-powered question generation, follow-up prompts, and answer evaluation
- Analytics dashboard for performance trends and weakness detection
- Adaptive study plans for 3-, 7-, and 30-day preparation
- Docker deploy artifacts and CI automation

## Technical Challenges
- Ensuring reliable LLM integration without breaking offline or test flows.
- Parsing and using resume content to inform question generation.
- Building a multi-step interview engine with state, question tracking, and answer evaluation.
- Designing a schema that supports interviews, responses, analytics, and study plans without overcomplicating the model.
- Securing the API and handling file uploads safely.

## Scalability
The architecture is designed to scale by separating concerns: backend services handle data and AI flows, while the frontend consumes APIs. For production, the DB can migrate from SQLite to PostgreSQL, file storage can move to S3, and the backend can run in containers behind a load balancer. A future scale plan includes caching prompt results, using managed LLM services, and adding asynchronous job queues for heavy analysis tasks.
