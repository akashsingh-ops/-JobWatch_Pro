from typing import Dict, Any
from apps.jobs.models import Job

class JobAnalyzerService:
    @staticmethod
    def analyze_job(job: Job) -> Dict[str, Any]:
        text = f"{job.title} {job.description}".lower()
        seniority = "Mid-Level"
        if "senior" in text or "lead" in text or "staff" in text:
            seniority = "Senior / Staff"
        elif "junior" in text or "entry" in text or "intern" in text:
            seniority = "Entry-Level"

        return {
            'job_id': str(job.id),
            'title': job.title,
            'seniority': seniority,
            'remote_classification': job.remote_type,
            'summary': job.description[:250] + "..." if len(job.description) > 250 else job.description
        }
