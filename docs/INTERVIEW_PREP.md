# Interview Preparation & Architecture Rationale

Why FastAPI?
- Lightweight, async-first, excellent developer ergonomics and production performance with Uvicorn.

Why React Native (Expo)?
- Single codebase for iOS/Android/Web demos and fast iteration using Expo.

Why Gemini?
- Gemini provides high-quality, controllable LLM responses for question generation and evaluation; the project keeps deterministic fallbacks for reliability.

Database choices
- SQLite for development simplicity; PostgreSQL recommended for production.

Scaling strategy
- Move to managed DB, run multiple backend replicas behind a load balancer, persist files to S3, and enable caching for prompt responses.
