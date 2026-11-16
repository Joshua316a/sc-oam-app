from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from core.database import Base
from api.models.base import BaseTimeStamped


class Blueprint(BaseTimeStamped, Base):
    """Blueprint ORM model."""

    __tablename__ = "blueprints"

    id = Column(Integer, primary_key=True, index=True)
    blueprint_id = Column(String, unique=True, index=True, nullable=False)
    bp_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    subcategory = Column(String, index=True)
    craft_type = Column(String, nullable=False)
    output_item_name = Column(String, nullable=False)
    quality_min = Column(Float, nullable=False, default=0.0)
    quality_max = Column(Float, nullable=False, default=1000.0)
    craft_time_seconds = Column(Float, nullable=False, default=0.0)
    ilg_label = Column(String, nullable=False)
    owner_handle = Column(String, nullable=True)
    acquired_date = Column(String, nullable=True)  # ISO format date string
    is_learned = Column(Boolean, nullable=False, default=False)
    notes = Column(String, nullable=True)