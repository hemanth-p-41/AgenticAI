"""Helpers to programmatically create or reset database schema.

This module is intended for development use (creating tables with SQLAlchemy's
`metadata.create_all`). Production schema changes should be performed with
Alembic migrations.
"""
from typing import Optional
from sqlalchemy.engine import Engine
from app.database.session import engine
from app.models.base import Base


def create_all(engine_override: Optional[Engine] = None) -> None:
    """Create all tables from SQLAlchemy models.

    Args:
        engine_override: Optional engine to use instead of the configured one.
    """
    eng = engine_override or engine
    Base.metadata.create_all(bind=eng)


def drop_all(engine_override: Optional[Engine] = None) -> None:
    """Drop all tables. Use carefully (development only)."""
    eng = engine_override or engine
    Base.metadata.drop_all(bind=eng)
