"""
Job Pydantic schemas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class Salary(BaseModel):
    """Salary information schema"""
    min: Optional[float] = None
    max: Optional[float] = None
    currency: str = "USD"


class JobBase(BaseModel):
    """Base job schema"""
    title: str
    company: str
    company_logo: Optional[str] = None
    location: str
    type: str  # Full-time, Part-time, Contract, Freelance, Internship
    remote: bool = False
    salary: Optional[Salary] = None
    description: str
    requirements: List[str] = []
    benefits: List[str] = []
    tags: List[str] = []
    expiry_date: Optional[datetime] = None
    application_url: Optional[str] = None
    apply_email: Optional[str] = None
    featured: bool = False


class JobCreate(JobBase):
    """Schema for job creation"""
    pass


class JobUpdate(BaseModel):
    """Schema for job updates"""
    title: Optional[str] = None
    company: Optional[str] = None
    company_logo: Optional[str] = None
    location: Optional[str] = None
    type: Optional[str] = None
    remote: Optional[bool] = None
    salary: Optional[Salary] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    expiry_date: Optional[datetime] = None
    application_url: Optional[str] = None
    apply_email: Optional[str] = None
    featured: Optional[bool] = None


class JobInDBBase(JobBase):
    """Base schema for job in database"""
    id: str
    posted_date: datetime
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Job(JobInDBBase):
    """Job schema for responses"""
    saved: bool = False


class JobInDB(JobInDBBase):
    """Job schema for database operations"""
    pass


class JobsResponse(BaseModel):
    """Response schema for jobs list"""
    jobs: List[Job]
    total: int
    page: int
    total_pages: int


class JobFilters(BaseModel):
    """Job filtering schema"""
    search: Optional[str] = None
    location: Optional[str] = None
    type: Optional[str] = None
    remote: Optional[bool] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    page: int = 1
    limit: int = 12


class SavedJob(BaseModel):
    """Saved job schema"""
    id: int
    job_id: str
    user_id: str
    saved_at: datetime
    job: Job

    class Config:
        from_attributes = True


class SaveJobRequest(BaseModel):
    """Save job request schema"""
    job_id: str
