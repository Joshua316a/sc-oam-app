import os

from api.models.base import BaseTimeStamped, Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

# ── Environment ─────────────────────────────────────────────
# Read from .env: DATABASE_URL="sqlite:///./database.db"
#             or DATABASE_URL="postgresql://user:pass@host:port/db"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# ── Engine ──────────────────────────────────────────────────
# SQLite uses connect_args for thread safety; PostgreSQL uses pool
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=None,  # NullPool for SQLite
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        echo=False,  # Set True for SQL debugging
    )

# ── Session ────────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ── ORM Base ────────────────────────────────────────────────
Base = declarative_base()

# ── Dependency ──────────────────────────────────────────────
def get_db() -> Generator:
    """FastAPI dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()