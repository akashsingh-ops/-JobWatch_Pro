"""
Job domain entity with comprehensive job management
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class JobStatus(Enum):
    """Job posting status"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
    EXPIRED = "expired"
    FILLED = "filled"


class EmploymentType(Enum):
    """Employment type"""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"


@dataclass
class SalaryRange:
    """Salary range value object"""
    min_salary: int
    max_salary: int
    currency: str = "USD"
    period: str = "yearly"  # yearly, monthly, hourly


@dataclass
class JobRequirement:
    """Job requirement value object"""
    skill: str
    proficiency_level: str  # beginner, intermediate, expert
    is_required: bool = True
    years_experience: Optional[int] = None


@dataclass
class JobBenefit:
    """Job benefit value object"""
    name: str
    description: Optional[str] = None
    category: str = "general"  # salary, health, work_life, professional_development, etc.


@dataclass
class ApplicationQuestion:
    """Custom application question"""
    question: str
    question_type: str  # text, textarea, select, multiselect, file
    is_required: bool = False
    options: List[str] = field(default_factory=list)  # For select/multiselect


class Job:
    """Job domain entity"""

    def __init__(self, job_id: str, title: str, company: str, posted_by: str):
        self.id = job_id
        self.title = title
        self.company = company
        self.posted_by = posted_by

        # Basic info
        self.description = ""
        self.short_description = ""
        self.category = ""
        self.subcategory = ""

        # Location and work type
        self.location = ""
        self.is_remote = False
        self.is_hybrid = False
        self.office_locations: List[str] = []

        # Employment details
        self.employment_type = EmploymentType.FULL_TIME
        self.experience_level = "mid_level"  # entry_level, mid_level, senior_level, expert_level
        self.industry = ""
        self.company_size = ""  # startup, small, medium, large, enterprise

        # Compensation
        self.salary_range: Optional[SalaryRange] = None
        self.show_salary = True
        self.equity_offered = False
        self.equity_details = ""

        # Requirements and skills
        self.requirements: List[JobRequirement] = []
        self.responsibilities: List[str] = []
        self.nice_to_have: List[str] = []

        # Benefits and perks
        self.benefits: List[JobBenefit] = []

        # Application settings
        self.application_deadline: Optional[datetime] = None
        self.application_questions: List[ApplicationQuestion] = []
        self.require_cover_letter = False
        self.require_portfolio = False
        self.require_resume = True

        # Status and metadata
        self.status = JobStatus.DRAFT
        self.featured = False
        self.urgent = False
        self.views_count = 0
        self.applications_count = 0

        # Timestamps
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.published_at: Optional[datetime] = None
        self.expires_at: Optional[datetime] = None

        # SEO and discoverability
        self.tags: List[str] = []
        self.keywords: List[str] = []

    def publish(self) -> 'JobPublished':
        """Publish the job posting"""
        if self.status != JobStatus.DRAFT:
            raise ValueError("Only draft jobs can be published")

        self.status = JobStatus.ACTIVE
        self.published_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        # Set default expiration (30 days from publish)
        if not self.expires_at:
            self.expires_at = self.published_at.replace(day=self.published_at.day + 30)

        from ..events.job_events import JobPublished
        return JobPublished(self.id, self.posted_by)

    def update(self, job_data: Dict[str, Any]) -> 'JobUpdated':
        """Update job details"""
        # Update basic fields
        for field in ['title', 'description', 'short_description', 'category',
                     'subcategory', 'location', 'is_remote', 'is_hybrid', 'industry']:
            if field in job_data:
                setattr(self, field, job_data[field])

        # Update employment type
        if 'employment_type' in job_data:
            self.employment_type = EmploymentType(job_data['employment_type'])

        # Update salary
        if 'salary_range' in job_data:
            self.salary_range = SalaryRange(**job_data['salary_range'])

        # Update requirements
        if 'requirements' in job_data:
            self.requirements = [JobRequirement(**req) for req in job_data['requirements']]

        # Update benefits
        if 'benefits' in job_data:
            self.benefits = [JobBenefit(**benefit) for benefit in job_data['benefits']]

        # Update tags and keywords
        if 'tags' in job_data:
            self.tags = job_data['tags']
        if 'keywords' in job_data:
            self.keywords = job_data['keywords']

        self.updated_at = datetime.utcnow()

        from ..events.job_events import JobUpdated
        return JobUpdated(self.id)

    def close(self) -> 'JobClosed':
        """Close the job posting"""
        if self.status not in [JobStatus.ACTIVE, JobStatus.PAUSED]:
            raise ValueError("Only active or paused jobs can be closed")

        self.status = JobStatus.CLOSED
        self.updated_at = datetime.utcnow()

        from ..events.job_events import JobClosed
        return JobClosed(self.id)

    def pause(self) -> 'JobPaused':
        """Pause the job posting"""
        if self.status != JobStatus.ACTIVE:
            raise ValueError("Only active jobs can be paused")

        self.status = JobStatus.PAUSED
        self.updated_at = datetime.utcnow()

        from ..events.job_events import JobPaused
        return JobPaused(self.id)

    def reactivate(self) -> 'JobReactivated':
        """Reactivate a paused job"""
        if self.status != JobStatus.PAUSED:
            raise ValueError("Only paused jobs can be reactivated")

        self.status = JobStatus.ACTIVE
        self.updated_at = datetime.utcnow()

        from ..events.job_events import JobReactivated
        return JobReactivated(self.id)

    def increment_views(self) -> None:
        """Increment view count"""
        self.views_count += 1

    def increment_applications(self) -> None:
        """Increment application count"""
        self.applications_count += 1

    def is_expired(self) -> bool:
        """Check if job has expired"""
        return self.expires_at and datetime.utcnow() > self.expires_at

    def matches_user_preferences(self, user_profile) -> bool:
        """Check if job matches user preferences"""
        if not user_profile or not user_profile.preferences:
            return True

        prefs = user_profile.preferences

        # Check location
        if prefs.preferred_locations and self.location not in prefs.preferred_locations:
            return False

        # Check employment type
        if prefs.contract_types and self.employment_type.value not in prefs.contract_types:
            return False

        # Check salary range
        if (prefs.salary_range_min and self.salary_range and
            self.salary_range.max_salary < prefs.salary_range_min):
            return False

        # Check remote work preference
        if prefs.remote_work and not self.is_remote:
            return False

        return True

    def get_required_skills(self) -> List[str]:
        """Get list of required skills"""
        return [req.skill for req in self.requirements if req.is_required]

    def get_nice_to_have_skills(self) -> List[str]:
        """Get list of nice-to-have skills"""
        return [req.skill for req in self.requirements if not req.is_required]

    def calculate_compatibility_score(self, user_profile) -> float:
        """Calculate job-user compatibility score (0-1)"""
        if not user_profile:
            return 0.5  # Neutral score for users without profiles

        score = 0.0
        factors = 0

        # Skills matching (40% weight)
        user_skills = user_profile.get_relevant_skills()
        required_skills = set(self.get_required_skills())
        nice_to_have_skills = set(self.get_nice_to_have_skills())

        if required_skills:
            required_matches = len(set(user_skills) & required_skills)
            score += (required_matches / len(required_skills)) * 0.4
            factors += 0.4

        # Nice-to-have skills (10% weight)
        if nice_to_have_skills:
            nice_matches = len(set(user_skills) & nice_to_have_skills)
            score += (nice_matches / len(nice_to_have_skills)) * 0.1
            factors += 0.1

        # Experience level (20% weight)
        user_exp_years = user_profile.calculate_experience_years()
        if self.experience_level == "entry_level" and user_exp_years <= 2:
            score += 0.2
        elif self.experience_level == "mid_level" and 2 <= user_exp_years <= 5:
            score += 0.2
        elif self.experience_level == "senior_level" and 5 <= user_exp_years <= 10:
            score += 0.2
        elif self.experience_level == "expert_level" and user_exp_years > 10:
            score += 0.2
        factors += 0.2

        # Location match (15% weight)
        if user_profile.profile.preferences and self.location in user_profile.profile.preferences.preferred_locations:
            score += 0.15
            factors += 0.15

        # Salary compatibility (15% weight)
        if (user_profile.profile.expected_salary and self.salary_range):
            if self.salary_range.min_salary <= user_profile.profile.expected_salary <= self.salary_range.max_salary:
                score += 0.15
            factors += 0.15

        return score / factors if factors > 0 else 0.0
