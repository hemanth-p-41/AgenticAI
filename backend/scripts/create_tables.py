"""Development helper to create database tables and print existing tables."""
from app.database.migrations import create_all, drop_all
from app.database.session import engine
from sqlalchemy import inspect


def main() -> None:
    # For development, drop and recreate to pick up model changes
    drop_all()
    create_all()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print('Created/Found tables:')
    for t in tables:
        print('-', t)


if __name__ == '__main__':
    main()
