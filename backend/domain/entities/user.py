"""
User domain entity with comprehensive profile management
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid


@dataclass
class UserProfile:
    """User profile value object"""
    skills: List['Skill'] = field(default_factory=list)
    experience: List['Experience'] = field(default_factory=list)
    education: List['Education'] = field(default_factory=list)
    preferences: 'JobPreferences' = None
    resume_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    current_salary: Optional[int] = None
    expected_salary: Optional[int] = None
    availability: str = "immediately"  # immediately, 2_weeks, 1_month, etc.


@dataclass
class Skill:
    """Skill value object"""
    name: str
    proficiency_level: str  # beginner, intermediate, expert
    years_experience: int
    endorsements: int = 0


@dataclass
class Experience:
    """Work experience value object"""
    company: str
    position: str
    location: str
    start_date: datetime
    end_date: Optional[datetime]
    is_current: bool = False
    description: str = ""
    technologies: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)


@dataclass
class Education:
    """Education value object"""
    institution: str
    degree: str
    field_of_study: str
    start_date: datetime
    end_date: Optional[datetime]
    grade: Optional[str] = None
    description: Optional[str] = None


@dataclass
class JobPreferences:
    """Job preferences value object"""
    desired_roles: List[str] = field(default_factory=list)
    preferred_locations: List[str] = field(default_factory=list)
    salary_range_min: Optional[int] = None
    salary_range_max: Optional[int] = None
    remote_work: bool = False
    contract_types: List[str] = field(default_factory=lambda: ["full_time", "part_time", "contract"])
    industries: List[str] = field(default_factory=list)
    company_sizes: List[str] = field(default_factory=list)  # startup, small, medium, large, enterprise


class User:
    """User domain entity"""

    def __init__(self, user_id: str, email: str, name: str):
        self.id = user_id
        self.email = email
        self.name = name
        self.profile = UserProfile()
        self.role = "candidate"  # candidate, employer, admin
        self.is_active = True
        self.is_verified = False
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.last_login = None
        self.email_notifications = True
        self.profile_visibility = "public"  # public, private, connections_only

    def update_profile(self, profile_data: Dict[str, Any]) -> 'UserProfileUpdated':
        """Update user profile with business logic validation"""
        # Validate skills
        if 'skills' in profile_data:
            validated_skills = []
            for skill_data in profile_data['skills']:
                if not skill_data.get('name'):
                    raise ValueError("Skill name is required")
                if skill_data.get('proficiency_level') not in ['beginner', 'intermediate', 'expert']:
                    raise ValueError("Invalid proficiency level")
                validated_skills.append(Skill(**skill_data))
            self.profile.skills = validated_skills

        # Validate experience
        if 'experience' in profile_data:
            validated_experience = []
            for exp_data in profile_data['experience']:
                if not exp_data.get('company') or not exp_data.get('position'):
                    raise ValueError("Company and position are required for experience")
                validated_experience.append(Experience(**exp_data))
            self.profile.experience = validated_experience

        # Update other profile fields
        for field in ['bio', 'location', 'phone', 'resume_url', 'linkedin_url',
                     'github_url', 'portfolio_url', 'current_salary', 'expected_salary']:
            if field in profile_data:
                setattr(self.profile, field, profile_data[field])

        # Update preferences
        if 'preferences' in profile_data:
            current_prefs = self.profile.preferences or JobPreferences()
            for key, value in profile_data['preferences'].items():
                if hasattr(current_prefs, key):
                    setattr(current_prefs, key, value)
            self.profile.preferences = current_prefs

        self.updated_at = datetime.utcnow()

        # Create domain event
        from ..events.user_events import UserProfileUpdated
        return UserProfileUpdated(self.id)

    def calculate_experience_years(self) -> int:
        """Calculate total years of experience"""
        total_months = 0

        for exp in self.profile.experience:
            start = exp.start_date
            end = exp.end_date or datetime.utcnow()

            # Calculate months between dates
            months = (end.year - start.year) * 12 + (end.month - start.month)
            total_months += max(0, months)

        return total_months // 12

    def get_relevant_skills(self) -> List[str]:
        """Get list of relevant skills for job matching"""
        skills = [skill.name for skill in self.profile.skills]

        # Add skills from experience
        for exp in self.profile.experience:
            skills.extend(exp.technologies)

        return list(set(skills))  # Remove duplicates

    def can_apply_for_job(self, job_requirements: Dict[str, Any]) -> bool:
        """Check if user meets basic job requirements"""
        # Check experience years
        if job_requirements.get('min_experience_years'):
            user_exp_years = self.calculate_experience_years()
            if user_exp_years < job_requirements['min_experience_years']:
                return False

        # Check required skills
        if job_requirements.get('required_skills'):
            user_skills = set(self.get_relevant_skills())
            required_skills = set(job_requirements['required_skills'])
            if not required_skills.issubset(user_skills):
                return False

        # Check location preference
        if job_requirements.get('location') and self.profile.preferences:
            if job_requirements['location'] not in self.profile.preferences.preferred_locations:
                return False

        return True

    def get_job_compatibility_score(self, job) -> float:
        """Calculate compatibility score with a job (0-1)"""
        score = 0.0
        factors = 0

        # Skills matching (40% weight)
        if hasattr(job, 'required_skills') and job.required_skills:
            user_skills = set(self.get_relevant_skills())
            job_skills = set(job.required_skills)
            skill_match = len(user_skills & job_skills) / len(job_skills)
            score += skill_match * 0.4
            factors += 0.4

        # Experience matching (25% weight)
        if hasattr(job, 'experience_level'):
            user_exp = self.calculate_experience_years()
            if job.experience_level == "entry_level" and user_exp <= 2:
                score += 0.25
            elif job.experience_level == "mid_level" and 2 <= user_exp <= 5:
                score += 0.25
            elif job.experience_level == "senior_level" and 5 <= user_exp <= 10:
                score += 0.25
            elif job.experience_level == "expert_level" and user_exp > 10:
                score += 0.25
            factors += 0.25

        # Location preference (20% weight)
        if self.profile.preferences and hasattr(job, 'location'):
            if job.location in self.profile.preferences.preferred_locations:
                score += 0.2
            factors += 0.2

        # Salary expectation (15% weight)
        if (self.profile.expected_salary and hasattr(job, 'salary_range') and job.salary_range):
            min_salary, max_salary = job.salary_range
            if min_salary <= self.profile.expected_salary <= max_salary:
                score += 0.15
            factors += 0.15

        return score / factors if factors > 0 else 0.0
