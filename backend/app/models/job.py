"""
Job database model
"""

from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, Float, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Job(Base):
    """
    Job posting model
    """
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    company_logo = Column(String, nullable=True)
    location = Column(String, nullable=False)
    type = Column(String, nullable=False)  # Full-time, Part-time, Contract, Freelance, Internship
    remote = Column(Boolean, default=False)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    currency = Column(String, default="USD")
    description = Column(Text, nullable=False)
    requirements = Column(JSON, default=list)  # List of requirements
    benefits = Column(JSON, default=list)  # List of benefits
    tags = Column(JSON, default=list)  # List of tags for categorization
    posted_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=True)
    application_url = Column(String, nullable=True)
    apply_email = Column(String, nullable=True)
    featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    saved_by_users = relationship("SavedJob", back_populates="job", cascade="all, delete-orphan")
    activities = relationship("UserActivity", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title}, company={self.company})>"


class SavedJob(Base):
    """
    Saved jobs relationship model
    """
    __tablename__ = "saved_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False)
    saved_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="saved_jobs")
    job = relationship("Job", back_populates="saved_by_users")

    def __repr__(self):
        return f"<SavedJob(user_id={self.user_id}, job_id={self.job_id})>"
