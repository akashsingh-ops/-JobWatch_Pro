"""
Advanced job recommendation system
"""

import math
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc

from app.models.user import User
from app.models.job import Job, SavedJob, JobApplication, UserActivity
from app.core.config import settings


class RecommendationService:
    """
    Advanced job recommendation system using multiple algorithms:
    1. Content-based filtering (skills, experience, preferences)
    2. Collaborative filtering (similar users)
    3. Behavioral analysis (user activity patterns)
    4. Hybrid scoring with machine learning readiness
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_recommendations_for_user(
        self,
        user_id: int,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get personalized job recommendations for a user
        """
        user = await self.db.get(User, user_id)
        if not user:
            return {"recommendations": [], "total": 0}

        # Get base job pool (active, non-expired jobs)
        base_jobs = await self._get_base_job_pool(user)

        # Score each job for this user
        scored_jobs = []
        for job in base_jobs:
            score, reasons, metadata = await self._calculate_job_score(user, job)
            if score > 0:  # Only include jobs with some relevance
                scored_jobs.append({
                    "job": job,
                    "score": score,
                    "reasons": reasons,
                    "metadata": metadata
                })

        # Sort by score (descending) and apply pagination
        scored_jobs.sort(key=lambda x: x["score"], reverse=True)
        total_recommendations = len(scored_jobs)

        # Apply pagination
        paginated_jobs = scored_jobs[offset:offset + limit]

        return {
            "recommendations": paginated_jobs,
            "total": total_recommendations,
            "has_more": (offset + limit) < total_recommendations,
            "user_profile_completeness": user.profile_completeness_score
        }

    async def _get_base_job_pool(self, user: User) -> List[Job]:
        """
        Get the base pool of jobs to recommend from
        """
        # Get jobs user hasn't already applied to or saved
        applied_job_ids = {app.job_id for app in user.job_applications}
        saved_job_ids = {saved.job_id for saved in user.saved_jobs}

        excluded_job_ids = applied_job_ids.union(saved_job_ids)

        query = select(Job).where(
            and_(
                Job.is_active == True,
                Job.is_deleted == False,
                Job.id.not_in(excluded_job_ids) if excluded_job_ids else True
            )
        ).order_by(desc(Job.created_at)).limit(1000)  # Limit for performance

        result = await self.db.execute(query)
        return result.scalars().all()

    async def _calculate_job_score(
        self,
        user: User,
        job: Job
    ) -> Tuple[float, List[str], Dict[str, Any]]:
        """
        Calculate recommendation score for a job-user pair
        Returns: (score, reasons, metadata)
        """
        score = 0.0
        reasons = []
        metadata = {}

        # 1. Skills Matching (35% weight)
        skill_score, skill_reasons, skill_metadata = self._calculate_skill_score(user, job)
        score += skill_score * 0.35
        reasons.extend(skill_reasons)
        metadata.update(skill_metadata)

        # 2. Experience & Level Matching (20% weight)
        exp_score, exp_reasons = self._calculate_experience_score(user, job)
        score += exp_score * 0.20
        reasons.extend(exp_reasons)

        # 3. Location Preferences (15% weight)
        location_score, location_reasons = self._calculate_location_score(user, job)
        score += location_score * 0.15
        reasons.extend(location_reasons)

        # 4. Salary Expectations (10% weight)
        salary_score, salary_reasons = self._calculate_salary_score(user, job)
        score += salary_score * 0.10
        reasons.extend(salary_reasons)

        # 5. Job Type Preferences (10% weight)
        job_type_score, job_type_reasons = self._calculate_job_type_score(user, job)
        score += job_type_score * 0.10
        reasons.extend(job_type_reasons)

        # 6. Company & Industry Match (5% weight)
        company_score, company_reasons = self._calculate_company_score(user, job)
        score += company_score * 0.05
        reasons.extend(company_reasons)

        # 7. Behavioral/Collaborative Filtering (5% weight)
        behavioral_score = await self._calculate_behavioral_score(user, job)
        score += behavioral_score * 0.05

        # 8. Freshness & Urgency Boost
        freshness_boost = self._calculate_freshness_boost(job)
        score += freshness_boost

        # 9. Profile Completeness Boost
        if user.is_profile_complete:
            score *= 1.1  # 10% boost for complete profiles
            reasons.append("Profile completeness bonus")

        # Ensure score doesn't exceed 100
        score = min(score, 100.0)

        return round(score, 2), reasons, metadata

    def _calculate_skill_score(self, user: User, job: Job) -> Tuple[float, List[str], Dict[str, Any]]:
        """
        Calculate skills matching score
        """
        user_skills = set(user.get_relevant_skills())
        required_skills = set(job.get_required_skills_list())
        preferred_skills = set(job.get_preferred_skills_list())

        if not required_skills:
            return 100.0, ["No specific skills required"], {"skill_match_ratio": 1.0}

        # Required skills match
        required_matches = len(user_skills.intersection(required_skills))
        required_ratio = required_matches / len(required_skills)

        # Preferred skills match
        preferred_matches = len(user_skills.intersection(preferred_skills))
        preferred_ratio = preferred_matches / max(len(preferred_skills), 1)

        # Combined score (required skills are more important)
        combined_score = (required_ratio * 0.7) + (preferred_ratio * 0.3)
        final_score = combined_score * 100

        reasons = []
        if required_matches > 0:
            reasons.append(f"{required_matches}/{len(required_skills)} required skills match")
        if preferred_matches > 0:
            reasons.append(f"{preferred_matches} preferred skills match")

        if final_score < 30:
            reasons.append("Limited skill alignment")
        elif final_score > 80:
            reasons.append("Excellent skill match")

        return final_score, reasons, {
            "required_skill_matches": required_matches,
            "preferred_skill_matches": preferred_matches,
            "skill_match_ratio": round(combined_score, 2)
        }

    def _calculate_experience_score(self, user: User, job: Job) -> Tuple[float, List[str]]:
        """
        Calculate experience level matching score
        """
        user_experience = user.years_of_experience or 0

        # Map experience levels to year ranges
        level_ranges = {
            "entry": (0, 2),
            "mid": (2, 5),
            "senior": (5, 10),
            "executive": (10, float('inf'))
        }

        required_range = level_ranges.get(job.experience_level, (0, float('inf')))
        min_exp, max_exp = required_range

        if min_exp <= user_experience <= max_exp:
            score = 100.0
            reasons = [f"Experience level matches ({job.experience_level})"]
        elif user_experience < min_exp:
            # Below minimum - partial score based on proximity
            if min_exp > 0:
                score = max(20, (user_experience / min_exp) * 60)
                reasons = [f"Below required experience (have {user_experience}y, need {min_exp}y+)"]
            else:
                score = 80.0
                reasons = ["Entry level position"]
        else:
            # Above maximum - still good match
            score = 90.0
            reasons = [f"Exceeds required experience (have {user_experience}y+)"]

        return score, reasons

    def _calculate_location_score(self, user: User, job: Job) -> Tuple[float, List[str]]:
        """
        Calculate location preference matching score
        """
        preferred_locations = user.get_preferred_locations()

        if not preferred_locations:
            # No location preferences set - assume open to all
            return 100.0, ["Open to all locations"]

        job_location = job.location.lower()
        preferred_lower = [loc.lower() for loc in preferred_locations]

        # Exact match
        if job_location in preferred_lower:
            return 100.0, ["Preferred location match"]

        # City match within preferred locations
        job_city = job.city.lower() if job.city else ""
        for pref_loc in preferred_lower:
            if job_city and job_city in pref_loc:
                return 80.0, ["City within preferred region"]

        # Country match
        if job.country.lower() in [loc.lower() for loc in preferred_locations]:
            return 60.0, ["Country match"]

        # Remote work consideration
        if job.remote_work and user.job_preferences.get("remote_ok", False):
            return 70.0, ["Remote work opportunity"]

        return 20.0, ["Location not in preferences"]

    def _calculate_salary_score(self, user: User, job: Job) -> Tuple[float, List[str]]:
        """
        Calculate salary expectation matching score
        """
        user_min_salary = user.get_salary_expectation()

        if not user_min_salary:
            return 100.0, ["No salary preference set"]

        if not job.salary_min:
            return 80.0, ["Salary not disclosed"]

        if user_min_salary <= job.salary_min:
            return 100.0, ["Salary meets or exceeds expectations"]
        elif user_min_salary <= job.salary_max:
            # Partial match
            ratio = (job.salary_max - user_min_salary) / (job.salary_max - job.salary_min)
            score = 60 + (ratio * 40)  # 60-100 range
            return score, ["Salary partially meets expectations"]
        else:
            return 20.0, ["Salary below expectations"]

    def _calculate_job_type_score(self, user: User, job: Job) -> Tuple[float, List[str]]:
        """
        Calculate job type preference matching score
        """
        preferred_types = user.job_preferences.get("job_types", []) if user.job_preferences else []

        if not preferred_types:
            return 100.0, ["Open to all job types"]

        if job.job_type in preferred_types:
            return 100.0, ["Preferred job type match"]

        return 30.0, ["Job type not in preferences"]

    def _calculate_company_score(self, user: User, job: Job) -> Tuple[float, List[str]]:
        """
        Calculate company/industry matching score
        """
        user_industry = user.industry
        company_industry = job.company_description  # Could be enhanced with industry classification

        if user_industry and company_industry and user_industry.lower() in company_industry.lower():
            return 100.0, ["Industry alignment"]

        # Could add company size, reputation, etc. matching here
        return 50.0, ["General company match"]

    async def _calculate_behavioral_score(self, user: User, job: Job) -> float:
        """
        Calculate behavioral/collaborative filtering score
        """
        # Find users similar to this user
        similar_users = await self._find_similar_users(user.id, limit=10)

        if not similar_users:
            return 0.0

        # See what jobs these similar users have applied to or saved
        similar_user_ids = [u["user_id"] for u in similar_users]

        query = select(JobApplication.job_id).where(
            and_(
                JobApplication.user_id.in_(similar_user_ids),
                JobApplication.job_id == job.id
            )
        )

        result = await self.db.execute(query)
        applications = result.scalars().all()

        # Calculate score based on similar user behavior
        if applications:
            # Weight by user similarity
            total_weight = sum(u["similarity"] for u in similar_users)
            score = min(len(applications) * 20, 100)  # Max 100 points
            return score

        return 0.0

    async def _find_similar_users(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Find users similar to the given user based on skills, experience, etc.
        """
        user = await self.db.get(User, user_id)
        if not user:
            return []

        # Simple similarity based on skills overlap
        # In production, this would use more sophisticated algorithms
        user_skills = set(user.get_relevant_skills())

        # Get all other users with their skills
        query = select(User).where(
            and_(
                User.id != user_id,
                User.is_active == True,
                User.is_deleted == False
            )
        ).limit(100)  # Limit for performance

        result = await self.db.execute(query)
        other_users = result.scalars().all()

        similar_users = []
        for other_user in other_users:
            other_skills = set(other_user.get_relevant_skills())
            if not other_skills:
                continue

            # Jaccard similarity for skills
            intersection = len(user_skills.intersection(other_skills))
            union = len(user_skills.union(other_skills))

            if union > 0:
                similarity = intersection / union
                if similarity > 0.1:  # Minimum similarity threshold
                    similar_users.append({
                        "user_id": other_user.id,
                        "similarity": similarity
                    })

        # Sort by similarity and return top matches
        similar_users.sort(key=lambda x: x["similarity"], reverse=True)
        return similar_users[:limit]

    def _calculate_freshness_boost(self, job: Job) -> float:
        """
        Calculate freshness boost for recent jobs
        """
        hours_old = (datetime.utcnow() - job.created_at).total_seconds() / 3600

        if hours_old < 24:  # Less than 1 day
            return 10.0
        elif hours_old < 72:  # Less than 3 days
            return 5.0
        elif hours_old < 168:  # Less than 1 week
            return 2.0

        return 0.0

    async def get_trending_jobs(self, limit: int = 10) -> List[Job]:
        """
        Get trending jobs based on recent activity
        """
        # Jobs with most applications/saves in the last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)

        query = select(Job).where(
            and_(
                Job.is_active == True,
                Job.is_deleted == False,
                Job.created_at >= week_ago
            )
        ).order_by(desc(Job.application_count + Job.save_count)).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_jobs_by_skills(self, skills: List[str], limit: int = 20) -> List[Job]:
        """
        Get jobs matching specific skills
        """
        query = select(Job).where(
            and_(
                Job.is_active == True,
                Job.is_deleted == False,
                # This would need a more sophisticated matching in production
                or_(*[Job.required_skills.contains(skill) for skill in skills])
            )
        ).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()
