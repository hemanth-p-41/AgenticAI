"""Database base helpers for Alembic and metadata export."""
from app.models.base import Base


def get_metadata():
    """Return SQLAlchemy MetaData for Alembic target metadata imports."""
    return Base.metadata
