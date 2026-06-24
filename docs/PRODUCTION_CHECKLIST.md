# Production Readiness Checklist

Security
- Ensure `SECRET_KEY` is set and rotated; do not commit secret keys to repo.
- Restrict CORS by setting `ALLOWED_ORIGINS` in environment.
- Serve backend over HTTPS (TLS termination at proxy/load balancer).
- Enable request size limits (`MAX_REQUEST_BODY`) and authentication rate-limiting where appropriate.

Deployment
- Use PostgreSQL in production; set `DATABASE_URL` accordingly.
- Run `alembic upgrade head` during deploy to apply migrations.
- Build and run containers via `docker compose` or in a cloud container service.

Monitoring & Logging
- Ensure logs are collected (rotate and ship logs); setup log aggregation (e.g., Datadog, ELK, Papertrail).
- Add error monitoring (Sentry) for uncaught exceptions and traces.

Backups & Data
- Backup production database regularly and test restores.
- Store uploaded resumes in durable object storage (S3) and enable lifecycle rules.

Operational
- Add health checks and readiness/liveness endpoints behind the load balancer.
- Prepare runbook for incident response (how to rotate keys, restore DB, scale services).

Environment variables (minimum)
- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `GEMINI_API_KEY` (if using Gemini)
- `ALLOWED_ORIGINS`
- `MAX_REQUEST_BODY`

CI/CD
- Add pipeline to run tests, linting, build images, and optionally deploy to staging for smoke tests.
