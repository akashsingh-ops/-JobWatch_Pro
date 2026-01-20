"""
Data record database model
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class Record(Base):
    """
    Data record model for storing various types of data entries
    """
    __tablename__ = "records"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    source = Column(String, nullable=False)  # Source of the data
    category = Column(String, nullable=False)  # Category classification
    published_date = Column(DateTime, nullable=False)
    url = Column(String, nullable=True)  # External URL if applicable
    is_active = Column(String, default="active")  # active, archived, deleted
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    activities = relationship("UserActivity", back_populates="record", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Record(id={self.id}, title={self.title}, category={self.category})>"
