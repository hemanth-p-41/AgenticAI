"""FastAPI application bootstrap.

Includes CORS setup, health check, and router registration placeholders.
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import os

from app.utils.logger import setup_logging
from app.config import SECRET_KEY


logger = setup_logging()

app = FastAPI(title='AI Interview Coach API', version='0.1.0')


class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_body_size: int = 10 * 1024 * 1024):
        super().__init__(app)
        self.max_body_size = max_body_size

    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        if len(body) > self.max_body_size:
            return JSONResponse({'detail': 'Request body too large'}, status_code=413)
        return await call_next(request)


# CORS - read allowed origins from env in production
allowed = os.getenv('ALLOWED_ORIGINS', '')
if allowed:
    allow_origins = [o.strip() for o in allowed.split(',') if o.strip()]
else:
    allow_origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Request size limits
app.add_middleware(BodySizeLimitMiddleware, max_body_size=int(os.getenv('MAX_REQUEST_BODY', str(10 * 1024 * 1024))))


@app.get('/health', tags=['health'])
def health() -> dict:
    return {'status': 'ok'}


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception('Unhandled exception: %s', exc)
    # sanitize error: do not leak internal details
    return JSONResponse({'detail': 'Internal server error'}, status_code=500)


# Register auth router explicitly; other routers will be added when implemented.
from app.routes import auth, resume, interview, evaluation, analytics, study_plan  # type: ignore

app.include_router(auth.router, prefix='/auth')
app.include_router(resume.router, prefix='/resume')
app.include_router(interview.router, prefix='/interview')
app.include_router(evaluation.router, prefix='/evaluation')
app.include_router(analytics.router, prefix='/analytics')
app.include_router(study_plan.router, prefix='/study-plan')

