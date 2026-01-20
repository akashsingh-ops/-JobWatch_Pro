"""
Job recommendation system - Advanced ML-ready recommendation engine
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import math
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class JobRecommendationService:
    """
    Advanced job recommendation service with ML-ready architecture

    Features:
    - Content-based filtering
    - Collaborative filtering preparation
    - User profile matching
    - Skills-based matching
    - Experience level matching
    - Location and preference matching
    - Real-time personalization
    """

    def __init__(self, user_repository, job_repository, application_repository):
        self.user_repo = user_repository
        self.job_repo = job_repository
        self.application_repo = application_repository

        # Recommendation weights (can be adjusted via ML)
        self.weights = {
            'skills_match': 0.35,
            'experience_match': 0.25,
            'location_match': 0.15,
            'salary_match': 0.10,
            'company_match': 0.05,
            'industry_match': 0.05,
            'application_history': 0.03,
            'popularity_boost': 0.02
        }

    def recommend_jobs_for_user(self, user_id: str, limit: int = 10,
                               context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Get personalized job recommendations for a user

        Args:
            user_id: User ID to get recommendations for
            limit: Maximum number of recommendations to return
            context: Additional context (current search, location, etc.)

        Returns:
            List of recommended jobs with scores and reasons
        """
        try:
            # Get user profile
            user = self.user_repo.find_by_id(user_id)
            if not user:
                return self._get_popular_jobs(limit)

            # Get user's application history
            user_applications = self.application_repo.find_by_user(user_id)
            applied_job_ids = {app.job_id for app in user_applications}

            # Get active jobs
            active_jobs = self.job_repo.find_active_jobs({})

            # Filter out already applied jobs
            available_jobs = [job for job in active_jobs if job.id not in applied_job_ids]

            if not available_jobs:
                return []

            # Calculate recommendation scores
            scored_jobs = []
            for job in available_jobs:
                score, reasons = self._calculate_recommendation_score(user, job, context)
                if score > 0:  # Only include jobs with positive scores
                    scored_jobs.append({
                        'job': job,
                        'score': score,
                        'reasons': reasons,
                        'rank': 0  # Will be set after sorting
                    })

            # Sort by score (descending)
            scored_jobs.sort(key=lambda x: x['score'], reverse=True)

            # Add ranking
            for i, item in enumerate(scored_jobs[:limit]):
                item['rank'] = i + 1

            # Log recommendation event
            self._log_recommendation_event(user_id, [item['job'].id for item in scored_jobs[:limit]])

            return scored_jobs[:limit]

        except Exception as e:
            logger.error(f"Error generating recommendations for user {user_id}: {str(e)}")
            return self._get_popular_jobs(limit)

    def _calculate_recommendation_score(self, user, job,
                                      context: Optional[Dict[str, Any]] = None) -> Tuple[float, List[str]]:
        """
        Calculate recommendation score for a user-job pair

        Returns:
            Tuple of (score, reasons_list)
        """
        score = 0.0
        reasons = []

        # Skills matching
        skills_score, skills_reasons = self._calculate_skills_score(user, job)
        score += skills_score * self.weights['skills_match']
        reasons.extend(skills_reasons)

        # Experience level matching
        exp_score, exp_reasons = self._calculate_experience_score(user, job)
        score += exp_score * self.weights['experience_match']
        reasons.extend(exp_reasons)

        # Location matching
        location_score, location_reasons = self._calculate_location_score(user, job)
        score += location_score * self.weights['location_match']
        reasons.extend(location_reasons)

        # Salary compatibility
        salary_score, salary_reasons = self._calculate_salary_score(user, job)
        score += salary_score * self.weights['salary_match']
        reasons.extend(salary_reasons)

        # Company/Industry matching
        company_score, company_reasons = self._calculate_company_score(user, job)
        score += company_score * self.weights['company_match']
        reasons.extend(company_reasons)

        # Industry matching
        industry_score, industry_reasons = self._calculate_industry_score(user, job)
        score += industry_score * self.weights['industry_match']
        reasons.extend(industry_reasons)

        # Application history patterns
        history_score, history_reasons = self._calculate_history_score(user, job)
        score += history_score * self.weights['application_history']
        reasons.extend(history_reasons)

        # Popularity boost for trending jobs
        popularity_score, popularity_reasons = self._calculate_popularity_score(job)
        score += popularity_score * self.weights['popularity_boost']
        reasons.extend(popularity_reasons)

        # Context-based adjustments
        if context:
            context_score, context_reasons = self._apply_context_adjustments(score, user, job, context)
            score = context_score
            reasons.extend(context_reasons)

        return score, reasons

    def _calculate_skills_score(self, user, job) -> Tuple[float, List[str]]:
        """Calculate skills matching score"""
        user_skills = set(user.get_relevant_skills())
        required_skills = set(job.get_required_skills())
        nice_to_have_skills = set(job.get_nice_to_have_skills())

        if not required_skills:
            return 0.5, ["Skills matching: No specific requirements"]

        # Required skills match
        required_matches = len(user_skills & required_skills)
        required_score = required_matches / len(required_skills)

        # Nice-to-have skills bonus
        nice_matches = len(user_skills & nice_to_have_skills)
        nice_score = nice_matches / max(len(nice_to_have_skills), 1) * 0.3

        total_score = min(1.0, required_score + nice_score)

        reasons = []
        if required_matches > 0:
            reasons.append(f"Matches {required_matches}/{len(required_skills)} required skills")
        if nice_matches > 0:
            reasons.append(f"Matches {nice_matches} nice-to-have skills")

        return total_score, reasons

    def _calculate_experience_score(self, user, job) -> Tuple[float, List[str]]:
        """Calculate experience level compatibility"""
        user_years = user.calculate_experience_years()
        job_level = job.experience_level

        # Map experience levels to year ranges
        level_ranges = {
            'entry_level': (0, 2),
            'mid_level': (2, 5),
            'senior_level': (5, 10),
            'expert_level': (10, float('inf'))
        }

        if job_level not in level_ranges:
            return 0.5, ["Experience level not specified"]

        min_years, max_years = level_ranges[job_level]

        if min_years <= user_years <= max_years:
            score = 1.0
            reason = f"Perfect experience match ({user_years} years for {job_level})"
        elif user_years < min_years:
            # Slightly below requirement
            score = max(0.3, user_years / min_years)
            reason = f"Experience slightly below requirement ({user_years} vs {min_years}+ years)"
        else:
            # Above requirement (still good)
            score = 0.8
            reason = f"Experience exceeds requirement ({user_years} vs {min_years}-{max_years} years)"

        return score, [reason]

    def _calculate_location_score(self, user, job) -> Tuple[float, List[str]]:
        """Calculate location compatibility"""
        if not user.profile.preferences or not user.profile.preferences.preferred_locations:
            return 0.7, ["Location preferences not specified"]

        preferred_locations = user.profile.preferences.preferred_locations

        if job.location in preferred_locations:
            return 1.0, [f"Perfect location match: {job.location}"]

        if job.is_remote:
            return 0.9, ["Remote work available"]

        # Check for nearby locations (simplified)
        for pref_location in preferred_locations:
            if self._are_locations_compatible(job.location, pref_location):
                return 0.8, [f"Nearby location: {job.location} near {pref_location}"]

        return 0.2, [f"Location mismatch: {job.location} not in preferences"]

    def _calculate_salary_score(self, user, job) -> Tuple[float, List[str]]:
        """Calculate salary compatibility"""
        if not user.profile.expected_salary or not job.salary_range:
            return 0.5, ["Salary information incomplete"]

        expected = user.profile.expected_salary
        job_min, job_max = job.salary_range.min_salary, job.salary_range.max_salary

        if job_min <= expected <= job_max:
            return 1.0, [f"Salary match: ${expected:,} within range"]

        if expected > job_max:
            ratio = job_max / expected
            score = max(0.1, ratio)
            return score, [f"Salary below expectation: ${job_max:,} vs ${expected:,}"]

        if expected < job_min:
            ratio = expected / job_min
            score = max(0.3, ratio)
            return score, [f"Salary above expectation: ${job_min:,} vs ${expected:,}"]

        return 0.5, ["Salary compatibility unclear"]

    def _calculate_company_score(self, user, job) -> Tuple[float, List[str]]:
        """Calculate company/employer matching"""
        # This could be enhanced with company preferences, past applications, etc.
        return 0.5, ["Company matching not implemented yet"]

    def _calculate_industry_score(self, user, job) -> Tuple[float, List[str]]:
        """Calculate industry compatibility"""
        if not user.profile.preferences or not user.profile.preferences.industries:
            return 0.5, ["Industry preferences not specified"]

        if job.industry in user.profile.preferences.industries:
            return 1.0, [f"Industry match: {job.industry}"]

        return 0.3, [f"Different industry: {job.industry}"]

    def _calculate_history_score(self, user, job) -> Tuple[float, List[str]]:
        """Calculate score based on application history patterns"""
        # This could analyze past successful applications
        return 0.0, []  # Not implemented yet

    def _calculate_popularity_score(self, job) -> Tuple[float, List[str]]:
        """Calculate popularity boost for trending jobs"""
        # Boost based on recent applications or views
        popularity_score = min(1.0, job.applications_count / 10)  # Simple popularity metric
        if popularity_score > 0.5:
            return popularity_score, [f"Popular job ({job.applications_count} applications)"]
        return 0.0, []

    def _apply_context_adjustments(self, base_score: float, user, job,
                                 context: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Apply context-based score adjustments"""
        score = base_score
        reasons = []

        # Current search context
        if context.get('current_search'):
            search_terms = set(context['current_search'].lower().split())
            job_text = f"{job.title} {job.description} {job.company}".lower()
            search_matches = len(search_terms & set(job_text.split()))
            if search_matches > 0:
                score += 0.2
                reasons.append(f"Matches current search terms")

        # Location context
        if context.get('current_location'):
            if job.location == context['current_location']:
                score += 0.1
                reasons.append(f"Location matches current search")

        # Recent activity boost
        if context.get('recent_activity'):
            # Boost jobs similar to recently viewed/applied jobs
            score += 0.05
            reasons.append("Based on recent activity")

        return score, reasons

    def _are_locations_compatible(self, loc1: str, loc2: str) -> bool:
        """Check if two locations are compatible (simplified)"""
        # This could use geocoding APIs for real distance calculation
        return loc1.lower() == loc2.lower()

    def _get_popular_jobs(self, limit: int) -> List[Dict[str, Any]]:
        """Get popular jobs when user profile is unavailable"""
        try:
            popular_jobs = self.job_repo.find_active_jobs({
                'sort_by': 'applications_count',
                'limit': limit
            })

            return [{
                'job': job,
                'score': 0.5,
                'reasons': ['Popular job'],
                'rank': i + 1
            } for i, job in enumerate(popular_jobs)]

        except Exception:
            return []

    def _log_recommendation_event(self, user_id: str, job_ids: List[str]) -> None:
        """Log recommendation event for analytics"""
        logger.info(f"Recommendations generated for user {user_id}: {len(job_ids)} jobs")

    # ML-Ready Methods (for future enhancement)
    def train_recommendation_model(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train ML model for better recommendations
        This is a placeholder for future ML integration
        """
        # This could integrate with scikit-learn, TensorFlow, etc.
        return {"status": "not_implemented", "message": "ML training not yet implemented"}

    def get_similar_jobs(self, job_id: str, limit: int = 5) -> List[str]:
        """
        Find jobs similar to a given job
        Useful for "more jobs like this" feature
        """
        try:
            job = self.job_repo.find_by_id(job_id)
            if not job:
                return []

            # Find jobs with similar skills and requirements
            similar_jobs = self.job_repo.find_active_jobs({
                'required_skills': job.get_required_skills()[:3],  # Top 3 skills
                'exclude_job_id': job_id,
                'limit': limit
            })

            return [j.id for j in similar_jobs]

        except Exception:
            return []

    def update_user_preferences_from_behavior(self, user_id: str) -> None:
        """
        Update user preferences based on their behavior
        ML-enhanced user profiling
        """
        # Analyze user's job views, applications, and patterns
        # Update preferences automatically
        pass
