"""
User models with comprehensive profile management
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from .base import Base, SoftDeleteMixin


class User(Base, SoftDeleteMixin):
    """
    User model with comprehensive profile management
    """

    __tablename__ = "users"

    # Authentication fields
    email: str = Column(String(255), unique=True, nullable=False, index=True)
    password_hash: str = Column(String(255), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    # Basic profile information
    first_name: str = Column(String(100), nullable=False)
    last_name: str = Column(String(100), nullable=False)
    phone: Optional[str] = Column(String(20))
    date_of_birth: Optional[datetime] = Column(DateTime)
    gender: Optional[str] = Column(String(20))
    profile_picture: Optional[str] = Column(String(500))

    # Professional information
    current_title: Optional[str] = Column(String(200))
    current_company: Optional[str] = Column(String(200))
    years_of_experience: Optional[float] = Column(Float)
    industry: Optional[str] = Column(String(100))
    bio: Optional[str] = Column(Text)

    # Skills and expertise
    skills: List[str] = Column(JSON, default=list)  # ["Python", "React", "AWS"]
    certifications: List[Dict[str, Any]] = Column(JSON, default=list)  # [{"name": "AWS Certified", "issuer": "Amazon", "date": "2023-01-01"}]

    # Education
    education: List[Dict[str, Any]] = Column(JSON, default=list)  # [{"degree": "B.Tech", "institution": "IIT", "year": 2020}]

    # Work experience
    work_experience: List[Dict[str, Any]] = Column(JSON, default=list)  # [{"title": "SDE", "company": "Google", "start_date": "2020-01", "end_date": "2023-01"}]

    # Job preferences
    job_preferences: Dict[str, Any] = Column(JSON, default=dict)  # {"locations": ["Bangalore", "Mumbai"], "job_types": ["Full-time"], "salary_min": 100000}

    # Resume and documents
    resume_url: Optional[str] = Column(String(500))
    portfolio_url: Optional[str] = Column(String(500))
    linkedin_url: Optional[str] = Column(String(500))
    github_url: Optional[str] = Column(String(500))

    # Privacy and communication preferences
    profile_visibility: str = Column(String(20), default="public")  # public, private, connections_only
    email_notifications: bool = Column(Boolean, default=True)
    sms_notifications: bool = Column(Boolean, default=False)
    push_notifications: bool = Column(Boolean, default=True)

    # Account status and metadata
    last_login: Optional[datetime] = Column(DateTime)
    login_attempts: int = Column(Integer, default=0)
    locked_until: Optional[datetime] = Column(DateTime)

    # Relationships
    job_applications = relationship("JobApplication", back_populates="user", cascade="all, delete-orphan")
    saved_jobs = relationship("SavedJob", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    activities = relationship("UserActivity", back_populates="user", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"

    @property
    def profile_completeness_score(self) -> float:
        """Calculate profile completeness score (0-100)"""
        fields = [
            self.current_title, self.current_company, self.bio, self.resume_url,
            self.skills, self.education, self.work_experience, self.job_preferences
        ]
        completed_fields = sum(1 for field in fields if field and (not isinstance(field, list) or len(field) > 0))
        return round((completed_fields / len(fields)) * 100, 1)

    @property
    def is_profile_complete(self) -> bool:
        """Check if profile is reasonably complete"""
        return self.profile_completeness_score >= 70

    def get_relevant_skills(self) -> List[str]:
        """Get skills relevant for job matching"""
        return self.skills or []

    def get_preferred_locations(self) -> List[str]:
        """Get preferred job locations"""
        return self.job_preferences.get("locations", []) if self.job_preferences else []

    def get_salary_expectation(self) -> Optional[int]:
        """Get minimum salary expectation"""
        return self.job_preferences.get("salary_min") if self.job_preferences else None

    def matches_job_criteria(self, job_skills: List[str], job_location: str, job_salary_min: Optional[int]) -> Dict[str, Any]:
        """
        Check how well user matches job criteria
        Returns match score and reasons
        """
        score = 0
        reasons = []

        # Skills matching (40% weight)
        user_skills = set(self.get_relevant_skills())
        job_skills_set = set(job_skills)
        skill_match = len(user_skills.intersection(job_skills_set))
        skill_score = (skill_match / max(len(job_skills_set), 1)) * 40
        score += skill_score

        if skill_match > 0:
            reasons.append(f"Skills match: {skill_match} skills")
        else:
            reasons.append("No skill matches")

        # Location matching (30% weight)
        preferred_locations = self.get_preferred_locations()
        if job_location in preferred_locations or not preferred_locations:
            score += 30
            reasons.append("Location preference match")
        else:
            reasons.append("Location not in preferences")

        # Salary matching (20% weight)
        user_salary_min = self.get_salary_expectation()
        if user_salary_min and job_salary_min:
            if user_salary_min <= job_salary_min:
                score += 20
                reasons.append("Salary expectation match")
            else:
                reasons.append("Salary below expectation")
        elif not user_salary_min:
            score += 10  # Partial score if no preference set
            reasons.append("No salary preference set")

        # Experience matching (10% weight)
        if self.years_of_experience and self.years_of_experience >= 1:
            score += 10
            reasons.append("Has work experience")
        else:
            reasons.append("Limited work experience")

        return {
            "score": round(score, 1),
            "reasons": reasons,
            "skill_match_ratio": round(skill_match / max(len(job_skills_set), 1), 2)
        }


class UserActivity(Base):
    """
    User activity tracking for analytics and recommendations
    """

    __tablename__ = "user_activities"

    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    activity_type: str = Column(String(50), nullable=False, index=True)  # view_job, apply_job, save_job, search, etc.
    entity_type: Optional[str] = Column(String(50))  # job, company, skill, etc.
    entity_id: Optional[str] = Column(String(100))  # ID of the entity
    metadata: Dict[str, Any] = Column(JSON, default=dict)  # Additional context
    ip_address: Optional[str] = Column(String(45))  # IPv4/IPv6
    user_agent: Optional[str] = Column(Text)

    # Relationships
    user = relationship("User", back_populates="activities")

    def __repr__(self):
        return f"<UserActivity(user_id={self.user_id}, type={self.activity_type})>"