"""
Jobs API endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.job import (
    Job, JobsResponse, JobFilters, SaveJobRequest
)
from app.services.job import JobService


router = APIRouter()


@router.get("/", response_model=JobsResponse)
async def get_jobs(
    search: str = Query(None, description="Search query"),
    location: str = Query(None, description="Job location"),
    type: str = Query(None, description="Job type"),
    remote: bool = Query(None, description="Remote work"),
    salary_min: float = Query(None, description="Minimum salary"),
    salary_max: float = Query(None, description="Maximum salary"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(12, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get jobs with filtering and pagination
    """
    try:
        filters = JobFilters(
            search=search,
            location=location,
            type=type,
            remote=remote,
            salary_min=salary_min,
            salary_max=salary_max,
            page=page,
            limit=limit
        )

        result = await JobService.get_jobs(db, filters, current_user.id)
        return JobsResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch jobs: {str(e)}")


@router.get("/{job_id}", response_model=Job)
async def get_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get job by ID
    """
    try:
        job = await JobService.get_job_by_id(db, job_id, current_user.id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        # Convert to response format
        job_dict = {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "company_logo": job.company_logo,
            "location": job.location,
            "type": job.type,
            "remote": job.remote,
            "salary": {
                "min": job.salary_min,
                "max": job.salary_max,
                "currency": job.currency
            } if job.salary_min or job.salary_max else None,
            "description": job.description,
            "requirements": job.requirements,
            "benefits": job.benefits,
            "tags": job.tags,
            "posted_date": job.posted_date,
            "expiry_date": job.expiry_date,
            "application_url": job.application_url,
            "apply_email": job.apply_email,
            "featured": job.featured,
            "saved": False  # Will be checked below
        }

        # Check if job is saved by user
        from app.models.job import SavedJob
        from sqlalchemy import select, and_
        result = await db.execute(
            select(SavedJob).where(
                and_(SavedJob.user_id == current_user.id, SavedJob.job_id == job_id)
            )
        )
        saved_job = result.scalar_one_or_none()
        job_dict["saved"] = saved_job is not None

        return Job(**job_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch job: {str(e)}")


@router.post("/save", response_model=dict)
async def save_job(
    job_data: SaveJobRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Save a job for the current user
    """
    try:
        await JobService.save_job(db, current_user.id, job_data.job_id)
        return {"message": "Job saved successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save job: {str(e)}")


@router.delete("/{job_id}/save", response_model=dict)
async def unsave_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Unsave a job for the current user
    """
    try:
        await JobService.unsave_job(db, current_user.id, job_id)
        return {"message": "Job unsaved successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to unsave job: {str(e)}")


@router.get("/saved/list", response_model=List[Job])
async def get_saved_jobs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get saved jobs for the current user
    """
    try:
        saved_jobs = await JobService.get_saved_jobs(db, current_user.id)
        return [Job(**job) for job in saved_jobs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch saved jobs: {str(e)}")


@router.get("/meta/categories", response_model=List[str])
async def get_job_categories(
    db: AsyncSession = Depends(get_db)
):
    """
    Get available job categories/tags
    """
    try:
        return await JobService.get_job_categories(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch categories: {str(e)}")


@router.get("/meta/types", response_model=List[str])
async def get_job_types(
    db: AsyncSession = Depends(get_db)
):
    """
    Get available job types
    """
    try:
        return await JobService.get_job_types(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch job types: {str(e)}")
