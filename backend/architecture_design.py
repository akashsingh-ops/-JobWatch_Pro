"""
Data Watch Nexus - Production-Grade Backend Architecture Design

This module contains the architectural design and implementation for a
scalable, production-ready job portal platform.

ARCHITECTURAL PRINCIPLES:
- Clean Architecture with clear separation of concerns
- Domain-Driven Design (DDD) principles
- SOLID principles
- Microservices-ready modular structure
- Comprehensive error handling and logging
- Security-first approach
- Scalability and maintainability

FOLDER STRUCTURE:
/backend
├── /api                    # API layer (controllers/routers)
│   ├── /v1                 # API version 1
│   ├── /middleware         # API middleware
│   └── /schemas            # API request/response schemas
├── /core                   # Core functionality
│   ├── /config             # Configuration management
│   ├── /database           # Database connection and setup
│   ├── /security           # Security utilities
│   ├── /logging            # Logging configuration
│   └── /cache              # Caching layer
├── /domain                 # Domain layer (business logic)
│   ├── /entities           # Domain entities
│   ├── /value_objects      # Value objects
│   ├── /repositories       # Repository interfaces
│   ├── /services           # Domain services
│   └── /events             # Domain events
├── /infrastructure         # Infrastructure layer
│   ├── /repositories       # Repository implementations
│   ├── /external           # External service integrations
│   ├── /messaging          # Message queue implementations
│   └── /storage            # File storage handlers
├── /application            # Application layer
│   ├── /services           # Application services
│   ├── /commands           # Command handlers
│   ├── /queries            # Query handlers
│   └── /events             # Application event handlers
├── /interfaces             # Interface adapters
│   ├── /controllers        # HTTP controllers
│   ├── /presenters         # Response formatters
│   ├── /middlewares        # HTTP middlewares
│   └── /validators         # Input validation
├── /utils                  # Shared utilities
├── /tests                  # Test suites
└── /docs                   # Documentation

KEY COMPONENTS:
1. Job Recommendation Engine
2. Job Application Management
3. User Profile System
4. Notification System
5. Email Service
6. Search and Filtering
7. Analytics and Reporting
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid

# Domain Events
class DomainEvent:
    """Base class for domain events"""
    event_id: str
    event_type: str
    timestamp: datetime
    aggregate_id: str

    def __init__(self, aggregate_id: str):
        self.event_id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow()
        self.aggregate_id = aggregate_id

# Value Objects
@dataclass
class Email:
    """Email value object"""
    address: str

    def __post_init__(self):
        if '@' not in self.address:
            raise ValueError("Invalid email format")

@dataclass
class Skill:
    """Skill value object"""
    name: str
    proficiency_level: str  # Beginner, Intermediate, Expert
    years_experience: int

@dataclass
class Experience:
    """Work experience value object"""
    company: str
    position: str
    start_date: datetime
    end_date: Optional[datetime]
    description: str
    technologies: List[str]

@dataclass
class JobPreferences:
    """Job preferences value object"""
    desired_roles: List[str]
    preferred_locations: List[str]
    salary_range_min: Optional[int]
    salary_range_max: Optional[int]
    remote_work: bool
    contract_types: List[str]  # Full-time, Part-time, Contract, etc.

# Domain Entities
class User:
    """User domain entity"""
    def __init__(self, user_id: str, email: Email, name: str):
        self.id = user_id
        self.email = email
        self.name = name
        self.profile = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.is_active = True
        self.role = UserRole.CANDIDATE

    def update_profile(self, profile_data: Dict[str, Any]) -> 'UserProfileUpdated':
        """Update user profile"""
        # Business logic for profile updates
        event = UserProfileUpdated(self.id)
        # Domain event publishing would go here
        return event

    def apply_for_job(self, job_id: str) -> 'JobApplicationSubmitted':
        """Apply for a job"""
        # Business logic validation
        event = JobApplicationSubmitted(self.id, job_id)
        return event

class Job:
    """Job domain entity"""
    def __init__(self, job_id: str, title: str, company: str, posted_by: str):
        self.id = job_id
        self.title = title
        self.company = company
        self.posted_by = posted_by
        self.description = ""
        self.requirements = []
        self.location = ""
        self.salary_range = None
        self.employment_type = EmploymentType.FULL_TIME
        self.status = JobStatus.ACTIVE
        self.posted_at = datetime.utcnow()
        self.expires_at = None

    def update_status(self, new_status: 'JobStatus') -> 'JobStatusUpdated':
        """Update job status"""
        event = JobStatusUpdated(self.id, new_status)
        return event

class JobApplication:
    """Job application domain entity"""
    def __init__(self, application_id: str, user_id: str, job_id: str):
        self.id = application_id
        self.user_id = user_id
        self.job_id = job_id
        self.status = ApplicationStatus.SUBMITTED
        self.applied_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.cover_letter = ""
        self.resume_url = ""

    def update_status(self, new_status: 'ApplicationStatus') -> 'ApplicationStatusUpdated':
        """Update application status"""
        event = ApplicationStatusUpdated(self.id, new_status)
        return event

# Enums
class UserRole(Enum):
    CANDIDATE = "candidate"
    EMPLOYER = "employer"
    ADMIN = "admin"

class EmploymentType(Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"

class JobStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
    EXPIRED = "expired"

class ApplicationStatus(Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    OFFERED = "offered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

# Domain Events
class UserProfileUpdated(DomainEvent):
    event_type = "user.profile.updated"
    def __init__(self, user_id: str):
        super().__init__(user_id)

class JobApplicationSubmitted(DomainEvent):
    event_type = "job.application.submitted"
    def __init__(self, user_id: str, job_id: str):
        super().__init__(user_id)
        self.job_id = job_id

class JobStatusUpdated(DomainEvent):
    event_type = "job.status.updated"
    def __init__(self, job_id: str, new_status: JobStatus):
        super().__init__(job_id)
        self.new_status = new_status

class ApplicationStatusUpdated(DomainEvent):
    event_type = "application.status.updated"
    def __init__(self, application_id: str, new_status: ApplicationStatus):
        super().__init__(application_id)
        self.new_status = new_status

class JobRecommended(DomainEvent):
    event_type = "job.recommended"
    def __init__(self, user_id: str, job_ids: List[str]):
        super().__init__(user_id)
        self.job_ids = job_ids

# Repository Interfaces (Contracts)
class IUserRepository:
    """User repository interface"""
    def save(self, user: User) -> None: pass
    def find_by_id(self, user_id: str) -> Optional[User]: pass
    def find_by_email(self, email: str) -> Optional[User]: pass
    def update(self, user: User) -> None: pass

class IJobRepository:
    """Job repository interface"""
    def save(self, job: Job) -> None: pass
    def find_by_id(self, job_id: str) -> Optional[Job]: pass
    def find_active_jobs(self, filters: Dict[str, Any]) -> List[Job]: pass
    def search_jobs(self, query: str, filters: Dict[str, Any]) -> List[Job]: pass

class IJobApplicationRepository:
    """Job application repository interface"""
    def save(self, application: JobApplication) -> None: pass
    def find_by_id(self, application_id: str) -> Optional[JobApplication]: pass
    def find_by_user_and_job(self, user_id: str, job_id: str) -> Optional[JobApplication]: pass
    def find_by_user(self, user_id: str) -> List[JobApplication]: pass
    def update_status(self, application_id: str, status: ApplicationStatus) -> None: pass

# Domain Services
class JobRecommendationService:
    """Job recommendation domain service"""

    def __init__(self, user_repo: IUserRepository, job_repo: IJobRepository):
        self.user_repo = user_repo
        self.job_repo = job_repo

    def recommend_jobs_for_user(self, user_id: str, limit: int = 10) -> List[str]:
        """
        Recommend jobs for a user based on:
        - User profile (skills, experience, preferences)
        - Job matching algorithms
        - Location preferences
        - Salary expectations
        - Employment type preferences
        """
        user = self.user_repo.find_by_id(user_id)
        if not user or not user.profile:
            # Return trending/popular jobs if no profile
            return self._get_trending_jobs(limit)

        # Extract user preferences and skills
        preferences = user.profile.preferences
        skills = user.profile.skills
        experience_years = user.profile.experience_years

        # Build recommendation criteria
        criteria = self._build_recommendation_criteria(preferences, skills, experience_years)

        # Find matching jobs
        recommended_jobs = self.job_repo.search_jobs("", criteria)

        # Apply ranking algorithm
        ranked_jobs = self._rank_jobs_by_relevance(recommended_jobs, user)

        # Return top job IDs
        return [job.id for job in ranked_jobs[:limit]]

    def _build_recommendation_criteria(self, preferences: JobPreferences,
                                     skills: List[Skill], experience_years: int) -> Dict[str, Any]:
        """Build search criteria for job recommendations"""
        criteria = {}

        if preferences:
            criteria['locations'] = preferences.preferred_locations
            criteria['employment_types'] = preferences.contract_types
            criteria['remote_work'] = preferences.remote_work
            if preferences.salary_range_min:
                criteria['salary_min'] = preferences.salary_range_min

        if skills:
            criteria['required_skills'] = [skill.name for skill in skills]

        if experience_years:
            criteria['experience_level'] = self._map_experience_to_level(experience_years)

        return criteria

    def _rank_jobs_by_relevance(self, jobs: List[Job], user: User) -> List[Job]:
        """Rank jobs by relevance to user profile"""
        scored_jobs = []

        for job in jobs:
            score = self._calculate_job_score(job, user)
            scored_jobs.append((job, score))

        # Sort by score (descending)
        scored_jobs.sort(key=lambda x: x[1], reverse=True)
        return [job for job, score in scored_jobs]

    def _calculate_job_score(self, job: Job, user: User) -> float:
        """Calculate relevance score for a job-user pair"""
        score = 0.0

        # Skills matching (40% weight)
        user_skills = [skill.name.lower() for skill in user.profile.skills]
        job_skills = [skill.lower() for skill in job.requirements]
        skill_matches = len(set(user_skills) & set(job_skills))
        score += (skill_matches / max(len(job_skills), 1)) * 0.4

        # Location preference (20% weight)
        if job.location in user.profile.preferences.preferred_locations:
            score += 0.2

        # Salary compatibility (15% weight)
        if user.profile.preferences.salary_range_min and job.salary_range:
            if job.salary_range[0] >= user.profile.preferences.salary_range_min:
                score += 0.15

        # Employment type match (15% weight)
        if job.employment_type.value in user.profile.preferences.contract_types:
            score += 0.15

        # Experience level match (10% weight)
        user_level = self._map_experience_to_level(user.profile.experience_years)
        if user_level in job.experience_level:
            score += 0.1

        return score

    def _map_experience_to_level(self, years: int) -> str:
        """Map years of experience to level"""
        if years < 2:
            return "entry_level"
        elif years < 5:
            return "mid_level"
        elif years < 10:
            return "senior_level"
        else:
            return "expert_level"

    def _get_trending_jobs(self, limit: int) -> List[str]:
        """Get trending/popular jobs when no user profile available"""
        # This would typically involve analytics/click tracking
        # For now, return recent active jobs
        trending_jobs = self.job_repo.find_active_jobs({
            'sort_by': 'posted_at',
            'limit': limit
        })
        return [job.id for job in trending_jobs]

class JobApplicationService:
    """Job application domain service"""

    def __init__(self, application_repo: IJobApplicationRepository,
                 user_repo: IUserRepository, job_repo: IJobRepository):
        self.application_repo = application_repo
        self.user_repo = user_repo
        self.job_repo = job_repo

    def submit_application(self, user_id: str, job_id: str,
                          cover_letter: str = "", resume_url: str = "") -> JobApplication:
        """Submit a job application"""

        # Validate user exists
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Validate job exists and is active
        job = self.job_repo.find_by_id(job_id)
        if not job or job.status != JobStatus.ACTIVE:
            raise ValueError("Job not found or not active")

        # Check if user already applied
        existing_application = self.application_repo.find_by_user_and_job(user_id, job_id)
        if existing_application:
            raise ValueError("User already applied for this job")

        # Create application
        application_id = str(uuid.uuid4())
        application = JobApplication(application_id, user_id, job_id)
        application.cover_letter = cover_letter
        application.resume_url = resume_url

        self.application_repo.save(application)

        return application

    def update_application_status(self, application_id: str,
                                new_status: ApplicationStatus,
                                updated_by: str) -> None:
        """Update application status"""
        application = self.application_repo.find_by_id(application_id)
        if not application:
            raise ValueError("Application not found")

        application.update_status(new_status)
        self.application_repo.update_status(application_id, new_status)

    def get_user_applications(self, user_id: str) -> List[JobApplication]:
        """Get all applications for a user"""
        return self.application_repo.find_by_user(user_id)

# Application Services (Use Cases)
class JobSearchService:
    """Application service for job search functionality"""

    def __init__(self, job_repo: IJobRepository, recommendation_service: JobRecommendationService):
        self.job_repo = job_repo
        self.recommendation_service = recommendation_service

    def search_jobs(self, query: str, filters: Dict[str, Any], user_id: Optional[str] = None) -> Dict[str, Any]:
        """Search jobs with optional personalization"""
        jobs = self.job_repo.search_jobs(query, filters)

        # If user is logged in, add relevance scores
        if user_id:
            user_recommendations = self.recommendation_service.recommend_jobs_for_user(user_id, limit=50)
            # Add recommendation boost to results
            jobs = self._boost_recommended_jobs(jobs, user_recommendations)

        return {
            'jobs': jobs,
            'total': len(jobs),
            'query': query,
            'filters': filters
        }

    def get_recommended_jobs(self, user_id: str, limit: int = 10) -> List[Job]:
        """Get personalized job recommendations"""
        recommended_job_ids = self.recommendation_service.recommend_jobs_for_user(user_id, limit)
        recommended_jobs = []

        for job_id in recommended_job_ids:
            job = self.job_repo.find_by_id(job_id)
            if job:
                recommended_jobs.append(job)

        return recommended_jobs

    def _boost_recommended_jobs(self, jobs: List[Job], recommended_ids: List[str]) -> List[Job]:
        """Boost recommended jobs in search results"""
        recommended_jobs = []
        other_jobs = []

        for job in jobs:
            if job.id in recommended_ids:
                recommended_jobs.append(job)
            else:
                other_jobs.append(job)

        return recommended_jobs + other_jobs

# Infrastructure implementations would go here
# (Database repositories, external service integrations, etc.)

if __name__ == "__main__":
    print("Data Watch Nexus - Domain Architecture Design")
    print("=" * 50)
    print("This module contains the domain model and business logic")
    print("for the job portal platform following Clean Architecture principles.")
