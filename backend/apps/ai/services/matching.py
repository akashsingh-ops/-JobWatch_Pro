from typing import Dict, List, Any
from apps.jobs.models import Job
from apps.profiles.models import Profile

class JobMatchingEngine:
    """
    Computes Candidate Profile ↔ Job Match Scores with reasoning and gap detection.
    """
    @staticmethod
    def calculate_match(profile: Profile, job: Job) -> Dict[str, Any]:
        user_skills = set([s.name.lower() for s in profile.skills.all()])
        job_skills = set([s.name.lower() for s in job.required_skills.all()])

        # If job has no tagged skills, parse from description/title
        if not job_skills:
            common_tags = ['react', 'typescript', 'python', 'django', 'postgresql', 'docker', 'aws', 'node.js', 'kubernetes', 'graphql', 'next.js', 'tailwind']
            desc_lower = (job.title + " " + job.description).lower()
            job_skills = set([tag for tag in common_tags if tag in desc_lower])

        matching_skills = user_skills.intersection(job_skills)
        missing_skills = job_skills - user_skills

        base_score = 60
        if job_skills:
            skill_match_ratio = len(matching_skills) / len(job_skills)
            base_score = int(40 + (skill_match_ratio * 50))
        else:
            base_score = 75

        # Category and location matching
        reasons = []
        if profile.headline and any(term in profile.headline.lower() for term in job.title.lower().split()):
            base_score = min(100, base_score + 10)
            reasons.append(f"Strong role alignment with your '{profile.headline}' experience.")

        if matching_skills:
            reasons.append(f"Direct match on key skills: {', '.join([s.title() for s in list(matching_skills)[:4]])}.")

        if job.remote_type == 'remote' or (profile.location and profile.location.lower() in job.location.lower()):
            reasons.append(f"Location preference matched ({job.location}).")

        recommendations = []
        if missing_skills:
            recommendations.append(f"Familiarity with {', '.join([s.title() for s in list(missing_skills)[:3]])} will strengthen your application.")
        else:
            recommendations.append("Your profile strongly matches all stated technical requirements for this role.")

        return {
            'score': max(50, min(98, base_score)),
            'reasons': reasons or ["Matches your software engineering profile."],
            'missing_skills': [s.title() for s in missing_skills],
            'matching_skills': [s.title() for s in matching_skills],
            'recommendations': recommendations
        }
