from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES = (
        ('saved', 'Saved'),
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied', db_index=True)
    applied_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at', '-created_at']
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.email} - {self.job.title} ({self.status})"
