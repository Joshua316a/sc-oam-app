from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Mixin providing created_at/updated_at columns
class BaseTimeStamped:
    """Mixin that adds created_at and updated_at timestamp columns."""
    
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="UTC timestamp when row was created",
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="UTC timestamp when row was last updated",
    )

# Declarative base for all SQLAlchemy models
Base = declarative_base()