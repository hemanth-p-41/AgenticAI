"""SQLAlchemy engine and session management (SQLAlchemy 2.0 style).

Provides:
- engine: SQLAlchemy Engine bound to DATABASE_URL
- SessionLocal: session factory
- get_db: FastAPI dependency yielding a Session
"""
from typing import Generator
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import DATABASE_URL

# SQLite needs a special connect arg
connect_args = {
    "check_same_thread": False
} if DATABASE_URL.startswith("sqlite") else {}

# Use future=True to enable SQLAlchemy 2.0 style behavior
engine = create_engine(DATABASE_URL, future=True, echo=False, connect_args=connect_args)

# Session factory configured for SQLAlchemy 2.0 usage
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a DB session and ensures it is closed.

    Yields:
        sqlalchemy.orm.Session: database session
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
