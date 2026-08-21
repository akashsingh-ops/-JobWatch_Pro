from django.db import models
from django.conf import settings
from apps.jobs.models import Job

class JobMatchScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_matches')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='candidate_matches')
    score = models.IntegerField(default=75, help_text='Match score percentage from 0 to 100')
    reasons = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-score']

    def __str__(self):
        return f"{self.user.email} ↔ {self.job.title}: {self.score}%"
