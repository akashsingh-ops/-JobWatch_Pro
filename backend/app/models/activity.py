"""
User activity and notification database models
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserActivity(Base):
    """
    User activity tracking model
    """
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    activity_type = Column(String, nullable=False)  # view_job, save_job, apply_job, view_record, etc.
    entity_type = Column(String, nullable=True)  # job, record, etc.
    entity_id = Column(String, nullable=True)  # ID of the entity
    description = Column(Text, nullable=True)
    metadata = Column(Text, nullable=True)  # Additional JSON metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="activities")
    job = relationship("Job", back_populates="activities")
    record = relationship("Record", back_populates="activities")

    def __repr__(self):
        return f"<UserActivity(user_id={self.user_id}, type={self.activity_type})>"


class Notification(Base):
    """
    User notification model
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String, nullable=False)  # info, warning, success, job_alert, system
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    action_url = Column(String, nullable=True)  # URL to redirect on click
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(user_id={self.user_id}, title={self.title}, read={self.is_read})>"
