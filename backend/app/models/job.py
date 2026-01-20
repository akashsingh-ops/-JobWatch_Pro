"""
Job models with comprehensive job management and application tracking
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import Column, String, Boolean, DateTime, Text, Float, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship

from .base import Base, SoftDeleteMixin


class Job(Base, SoftDeleteMixin):
    """
    Job posting model with comprehensive job information
    """

    __tablename__ = "jobs"

    # Basic job information
    title: str = Column(String(200), nullable=False, index=True)
    company_name: str = Column(String(200), nullable=False, index=True)
    company_logo: Optional[str] = Column(String(500))
    company_website: Optional[str] = Column(String(500))
    company_description: Optional[str] = Column(Text)

    # Job details
    description: str = Column(Text, nullable=False)
    requirements: List[str] = Column(Text, nullable=False)  # JSON string of requirements
    responsibilities: List[str] = Column(Text, default="[]")  # JSON string
    benefits: List[str] = Column(Text, default="[]")  # JSON string

    # Job specifications
    job_type: str = Column(String(50), nullable=False, index=True)  # Full-time, Part-time, Contract, etc.
    experience_level: str = Column(String(50), default="entry")  # entry, mid, senior, executive
    remote_work: bool = Column(Boolean, default=False, index=True)
    hybrid_work: bool = Column(Boolean, default=False)

    # Location information
    location: str = Column(String(200), nullable=False, index=True)
    country: str = Column(String(100), default="India")
    city: str = Column(String(100))
    postal_code: Optional[str] = Column(String(20))

    # Salary information
    salary_min: Optional[float] = Column(Float)
    salary_max: Optional[float] = Column(Float)
    salary_currency: str = Column(String(10), default="INR")
    salary_period: str = Column(String(20), default="yearly")  # yearly, monthly, hourly
    salary_negotiable: bool = Column(Boolean, default=True)

    # Skills and keywords
    required_skills: List[str] = Column(Text, default="[]")  # JSON string
    preferred_skills: List[str] = Column(Text, default="[]")  # JSON string
    keywords: List[str] = Column(Text, default="[]")  # JSON string for search

    # Application settings
    application_deadline: Optional[datetime] = Column(DateTime)
    application_url: Optional[str] = Column(String(500))
    application_email: Optional[str] = Column(String(255))
    contact_person: Optional[str] = Column(String(200))
    contact_email: Optional[str] = Column(String(255))

    # Job status and visibility
    is_active: bool = Column(Boolean, default=True, index=True)
    is_featured: bool = Column(Boolean, default=False, index=True)
    is_urgent: bool = Column(Boolean, default=False)
    priority: int = Column(Integer, default=0)  # Higher number = higher priority

    # Analytics and metrics
    view_count: int = Column(Integer, default=0)
    application_count: int = Column(Integer, default=0)
    save_count: int = Column(Integer, default=0)

    # Posting information
    posted_by_id: Optional[int] = Column(Integer, ForeignKey("users.id"), index=True)
    posted_by_name: Optional[str] = Column(String(200))

    # Relationships
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")
    saved_by_users = relationship("SavedJob", back_populates="job", cascade="all, delete-orphan")

    # Indexes for performance
    __table_args__ = (
        Index('idx_job_location_type', 'location', 'job_type'),
        Index('idx_job_skills', 'required_skills'),
        Index('idx_job_active_featured', 'is_active', 'is_featured'),
        Index('idx_job_posted_date', 'created_at'),
    )

    @property
    def salary_range_display(self) -> str:
        """Get formatted salary range for display"""
        if not self.salary_min and not self.salary_max:
            return "Salary not disclosed"

        currency_symbol = "₹" if self.salary_currency == "INR" else "$"

        if self.salary_min and self.salary_max:
            return f"{currency_symbol}{self.salary_min:,.0f} - {currency_symbol}{self.salary_max:,.0f} per {self.salary_period}"
        elif self.salary_min:
            return f"From {currency_symbol}{self.salary_min:,.0f} per {self.salary_period}"
        else:
            return f"Up to {currency_symbol}{self.salary_max:,.0f} per {self.salary_period}"

    @property
    def time_since_posted(self) -> str:
        """Get human-readable time since job was posted"""
        now = datetime.utcnow()
        diff = now - self.created_at

        if diff.days > 365:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
        elif diff.days > 30:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"

    @property
    def is_expired(self) -> bool:
        """Check if job posting has expired"""
        if self.application_deadline:
            return datetime.utcnow() > self.application_deadline
        return False

    def get_required_skills_list(self) -> List[str]:
        """Get required skills as list"""
        try:
            import json
            return json.loads(self.required_skills) if self.required_skills else []
        except:
            return []

    def get_preferred_skills_list(self) -> List[str]:
        """Get preferred skills as list"""
        try:
            import json
            return json.loads(self.preferred_skills) if self.preferred_skills else []
        except:
            return []

    def get_keywords_list(self) -> List[str]:
        """Get keywords as list"""
        try:
            import json
            return json.loads(self.keywords) if self.keywords else []
        except:
            return []

    def matches_user_profile(self, user) -> Dict[str, Any]:
        """
        Check how well this job matches a user profile
        Returns match score and reasons
        """
        if not user:
            return {"score": 0, "reasons": ["No user profile available"]}

        return user.matches_job_criteria(
            self.get_required_skills_list(),
            self.location,
            self.salary_min
        )


class JobApplication(Base):
    """
    Job application tracking model
    """

    __tablename__ = "job_applications"

    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    job_id: int = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)

    # Application status
    status: str = Column(String(50), default="applied", index=True)  # applied, under_review, interview_scheduled, rejected, accepted, withdrawn
    status_changed_at: datetime = Column(DateTime, default=datetime.utcnow)
    status_changed_by: Optional[int] = Column(Integer, ForeignKey("users.id"))  # Who changed the status

    # Application content
    cover_letter: Optional[str] = Column(Text)
    expected_salary: Optional[float] = Column(Float)
    available_from: Optional[datetime] = Column(DateTime)
    additional_notes: Optional[str] = Column(Text)

    # Resume and documents
    resume_url: Optional[str] = Column(String(500))
    portfolio_url: Optional[str] = Column(String(500))
    additional_documents: List[str] = Column(Text, default="[]")  # JSON string of additional document URLs

    # Tracking
    applied_via: str = Column(String(50), default="platform")  # platform, email, external_url
    source: str = Column(String(100), default="job_search")  # job_search, recommendation, email, etc.

    # Relationships
    user = relationship("User", back_populates="job_applications")
    job = relationship("Job", back_populates="applications")

    # Indexes
    __table_args__ = (
        Index('idx_application_user_job', 'user_id', 'job_id', unique=True),
        Index('idx_application_status', 'status'),
        Index('idx_application_date', 'created_at'),
    )

    @property
    def status_display(self) -> str:
        """Get human-readable status"""
        status_map = {
            "applied": "Application Submitted",
            "under_review": "Under Review",
            "interview_scheduled": "Interview Scheduled",
            "rejected": "Application Rejected",
            "accepted": "Application Accepted",
            "withdrawn": "Application Withdrawn"
        }
        return status_map.get(self.status, self.status.replace("_", " ").title())

    def can_change_status(self, new_status: str, user_id: int) -> bool:
        """
        Check if user can change application status
        """
        # Users can only withdraw their own applications
        if new_status == "withdrawn":
            return self.user_id == user_id

        # Employers/recruiters can change other statuses
        return self.user_id != user_id

    def update_status(self, new_status: str, changed_by: int) -> None:
        """Update application status"""
        self.status = new_status
        self.status_changed_at = datetime.utcnow()
        self.status_changed_by = changed_by


class SavedJob(Base):
    """
    Saved jobs relationship model
    """

    __tablename__ = "saved_jobs"

    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    job_id: int = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)

    # Additional metadata
    notes: Optional[str] = Column(Text)  # User's notes about why they saved this job
    reminder_date: Optional[datetime] = Column(DateTime)  # When to remind user about this job

    # Relationships
    user = relationship("User", back_populates="saved_jobs")
    job = relationship("Job", back_populates="saved_by_users")

    # Unique constraint
    __table_args__ = (
        Index('idx_saved_job_unique', 'user_id', 'job_id', unique=True),
    )