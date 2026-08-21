from typing import List
from apps.jobs.models import Job
from apps.profiles.models import Profile

class AIRecommendationService:
    @staticmethod
    def get_recommendations(profile: Profile, limit: int = 6) -> List[Job]:
        user_skills = profile.skills.all()
        if user_skills.exists():
            matched_jobs = Job.objects.filter(
                is_active=True,
                required_skills__in=user_skills
            ).distinct().select_related('company')[:limit]
            if matched_jobs.exists():
                return list(matched_jobs)

        return list(Job.objects.filter(is_active=True).select_related('company')[:limit])
