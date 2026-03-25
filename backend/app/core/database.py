"""
database.py — compatibility shim.

All data access has been migrated to the Supabase REST SDK
(see app/core/supabase_client.py).

A lightweight in-memory SQLite engine is used purely so that:
  - `models.Base.metadata.create_all(bind=engine)` in main.py doesn't crash
  - Alembic / model imports keep working
The engine never touches a real Postgres database.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Always use an in-memory SQLite dummy — no real DB connection needed.
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency — yields None; services use Supabase SDK directly."""
    yield None
