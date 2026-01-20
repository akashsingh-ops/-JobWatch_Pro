"""
Job service for managing job postings
"""

import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc, func
from fastapi import HTTPException

from app.models.job import Job, SavedJob
from app.schemas.job import JobCreate, JobUpdate, JobFilters, SaveJobRequest
from app.core.elasticsearch import index_job, search_jobs
from app.services.activity import create_activity


class JobService:
    """Job service class"""

    @staticmethod
    async def create_job(db: AsyncSession, job_data: JobCreate) -> Job:
        """
        Create a new job posting
        """
        job_id = str(uuid.uuid4())

        # Convert salary dict to database format
        salary_data = None
        if job_data.salary:
            salary_data = {
                "min": job_data.salary.min,
                "max": job_data.salary.max,
                "currency": job_data.salary.currency
            }

        job = Job(
            id=job_id,
            title=job_data.title,
            company=job_data.company,
            company_logo=job_data.company_logo,
            location=job_data.location,
            type=job_data.type,
            remote=job_data.remote,
            salary_min=salary_data.get("min") if salary_data else None,
            salary_max=salary_data.get("max") if salary_data else None,
            currency=salary_data.get("currency", "USD") if salary_data else "USD",
            description=job_data.description,
            requirements=job_data.requirements,
            benefits=job_data.benefits,
            tags=job_data.tags,
            expiry_date=job_data.expiry_date,
            application_url=job_data.application_url,
            apply_email=job_data.apply_email,
            featured=job_data.featured
        )

        db.add(job)
        await db.commit()
        await db.refresh(job)

        # Index in Elasticsearch for search
        job_dict = {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "company_logo": job.company_logo,
            "location": job.location,
            "type": job.type,
            "remote": job.remote,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "currency": job.currency,
            "description": job.description,
            "requirements": job.requirements,
            "benefits": job.benefits,
            "tags": job.tags,
            "posted_date": job.posted_date.isoformat() if job.posted_date else None,
            "expiry_date": job.expiry_date.isoformat() if job.expiry_date else None,
            "featured": job.featured,
            "category": job.tags[0] if job.tags else "general"
        }
        await index_job(job_dict)

        return job

    @staticmethod
    async def get_jobs(
        db: AsyncSession,
        filters: JobFilters,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get jobs with filtering and pagination
        """
        # For now, use Elasticsearch for search if available
        # Fall back to database search
        try:
            search_filters = {}
            if filters.location:
                search_filters["location"] = filters.location
            if filters.type:
                search_filters["type"] = filters.type
            if filters.remote is not None:
                search_filters["remote"] = filters.remote
            if filters.salary_min:
                search_filters["salary_min"] = filters.salary_min
            if filters.salary_max:
                search_filters["salary_max"] = filters.salary_max

            search_result = await search_jobs(
                query=filters.search or "",
                filters=search_filters,
                page=filters.page,
                limit=filters.limit
            )

            # Get saved job status for user
            if user_id and search_result["jobs"]:
                job_ids = [job["id"] for job in search_result["jobs"]]
                saved_result = await db.execute(
                    select(SavedJob.job_id).where(
                        and_(
                            SavedJob.user_id == user_id,
                            SavedJob.job_id.in_(job_ids)
                        )
                    )
                )
                saved_job_ids = {row[0] for row in saved_result.fetchall()}

                # Mark jobs as saved
                for job in search_result["jobs"]:
                    job["saved"] = job["id"] in saved_job_ids

            return search_result

        except Exception as e:
            print(f"Elasticsearch search failed: {e}")
            # Fall back to database search
            return await JobService._get_jobs_from_db(db, filters, user_id)

    @staticmethod
    async def _get_jobs_from_db(
        db: AsyncSession,
        filters: JobFilters,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get jobs from database as fallback
        """
        query = select(Job).where(Job.is_active == True)

        # Apply filters
        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.where(
                or_(
                    Job.title.ilike(search_term),
                    Job.company.ilike(search_term),
                    Job.description.ilike(search_term),
                    Job.tags.cast(String).ilike(search_term)
                )
            )

        if filters.location:
            query = query.where(Job.location.ilike(f"%{filters.location}%"))

        if filters.type:
            query = query.where(Job.type == filters.type)

        if filters.remote is not None:
            query = query.where(Job.remote == filters.remote)

        if filters.salary_min:
            query = query.where(Job.salary_min >= filters.salary_min)

        if filters.salary_max:
            query = query.where(Job.salary_max <= filters.salary_max)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply pagination
        query = query.order_by(desc(Job.posted_date))
        query = query.limit(filters.limit).offset((filters.page - 1) * filters.limit)

        result = await db.execute(query)
        jobs = result.scalars().all()

        # Get saved job status
        saved_jobs = []
        if user_id:
            job_ids = [job.id for job in jobs]
            if job_ids:
                saved_result = await db.execute(
                    select(SavedJob.job_id).where(
                        and_(
                            SavedJob.user_id == user_id,
                            SavedJob.job_id.in_(job_ids)
                        )
                    )
                )
                saved_job_ids = {row[0] for row in saved_result.fetchall()}
                saved_jobs = list(saved_job_ids)

        # Convert to response format
        jobs_list = []
        for job in jobs:
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
                "posted_date": job.posted_date.isoformat() if job.posted_date else None,
                "expiry_date": job.expiry_date.isoformat() if job.expiry_date else None,
                "application_url": job.application_url,
                "apply_email": job.apply_email,
                "featured": job.featured,
                "saved": job.id in saved_jobs
            }
            jobs_list.append(job_dict)

        total_pages = (total + filters.limit - 1) // filters.limit

        return {
            "jobs": jobs_list,
            "total": total,
            "page": filters.page,
            "total_pages": total_pages
        }

    @staticmethod
    async def get_job_by_id(db: AsyncSession, job_id: str, user_id: Optional[str] = None) -> Optional[Job]:
        """
        Get job by ID
        """
        result = await db.execute(select(Job).where(Job.id == job_id))
        job = result.scalar_one_or_none()

        if job and user_id:
            # Log view activity
            await create_activity(
                db=db,
                user_id=user_id,
                activity_type="view_job",
                entity_type="job",
                entity_id=job_id,
                description=f"Viewed job: {job.title}"
            )

        return job

    @staticmethod
    async def save_job(db: AsyncSession, user_id: str, job_id: str) -> SavedJob:
        """
        Save a job for a user
        """
        # Check if already saved
        result = await db.execute(
            select(SavedJob).where(
                and_(SavedJob.user_id == user_id, SavedJob.job_id == job_id)
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=400, detail="Job already saved")

        # Check if job exists
        job_result = await db.execute(select(Job).where(Job.id == job_id))
        job = job_result.scalar_one_or_none()

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        saved_job = SavedJob(user_id=user_id, job_id=job_id)
        db.add(saved_job)
        await db.commit()
        await db.refresh(saved_job)

        # Log save activity
        await create_activity(
            db=db,
            user_id=user_id,
            activity_type="save_job",
            entity_type="job",
            entity_id=job_id,
            description=f"Saved job: {job.title}"
        )

        return saved_job

    @staticmethod
    async def unsave_job(db: AsyncSession, user_id: str, job_id: str) -> bool:
        """
        Unsave a job for a user
        """
        result = await db.execute(
            select(SavedJob).where(
                and_(SavedJob.user_id == user_id, SavedJob.job_id == job_id)
            )
        )
        saved_job = result.scalar_one_or_none()

        if not saved_job:
            raise HTTPException(status_code=404, detail="Saved job not found")

        await db.delete(saved_job)
        await db.commit()

        # Log unsave activity
        await create_activity(
            db=db,
            user_id=user_id,
            activity_type="unsave_job",
            entity_type="job",
            entity_id=job_id,
            description=f"Unsaved job"
        )

        return True

    @staticmethod
    async def get_saved_jobs(db: AsyncSession, user_id: str) -> List[Dict[str, Any]]:
        """
        Get saved jobs for a user
        """
        result = await db.execute(
            select(SavedJob, Job)
            .join(Job, SavedJob.job_id == Job.id)
            .where(SavedJob.user_id == user_id)
            .order_by(desc(SavedJob.saved_at))
        )

        saved_jobs = []
        for saved_job, job in result:
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
                "posted_date": job.posted_date.isoformat() if job.posted_date else None,
                "application_url": job.application_url,
                "apply_email": job.apply_email,
                "featured": job.featured,
                "saved": True,
                "saved_at": saved_job.saved_at.isoformat()
            }
            saved_jobs.append(job_dict)

        return saved_jobs

    @staticmethod
    async def get_job_categories(db: AsyncSession) -> List[str]:
        """
        Get unique job categories/tags
        """
        result = await db.execute(
            select(Job.tags).where(Job.is_active == True)
        )

        all_tags = []
        for row in result.fetchall():
            if row[0]:  # tags list
                all_tags.extend(row[0])

        return list(set(all_tags))

    @staticmethod
    async def get_job_types(db: AsyncSession) -> List[str]:
        """
        Get unique job types
        """
        result = await db.execute(
            select(Job.type).where(Job.is_active == True).distinct()
        )

        return [row[0] for row in result.fetchall()]
