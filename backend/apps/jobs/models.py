from django.db import models
from django.utils import timezone
from apps.companies.models import Company
from apps.skills.models import Skill
import uuid

class Job(models.Model):
    EMPLOYMENT_CHOICES = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Remote', 'Remote'),
        ('Internship', 'Internship'),
    )

    EXPERIENCE_CHOICES = (
        ('Entry', 'Entry'),
        ('Mid', 'Mid'),
        ('Senior', 'Senior'),
        ('Lead', 'Lead'),
    )

    REMOTE_CHOICES = (
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('onsite', 'On-site'),
    )

    id = models.CharField(max_length=64, primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    location = models.CharField(max_length=200, db_index=True)
    category = models.CharField(max_length=100, db_index=True, default='Engineering')
    remote_type = models.CharField(max_length=20, choices=REMOTE_CHOICES, default='remote')
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_CHOICES, default='Full-time', db_index=True)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES, default='Mid', db_index=True)

    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=10, default='USD')
    salary = models.CharField(max_length=100, blank=True, default='$120,000 - $160,000')

    application_url = models.URLField(blank=True, default='https://example.com/apply')
    source = models.CharField(max_length=100, default='direct', db_index=True)
    source_job_id = models.CharField(max_length=200, blank=True, db_index=True)

    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)
    required_skills = models.ManyToManyField(Skill, related_name='jobs', blank=True)
    requirements = models.JSONField(default=list, blank=True)

    posted_at = models.DateTimeField(default=timezone.now, db_index=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted_at', '-created_at']
        indexes = [
            models.Index(fields=['title', 'category', 'is_active']),
            models.Index(fields=['employment_type', 'experience_level', 'is_active']),
            models.Index(fields=['source', 'source_job_id']),
        ]

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    @property
    def posted_date_formatted(self):
        now = timezone.now()
        diff = now - self.posted_at
        if diff.days == 0:
            hours = diff.seconds // 3600
            if hours == 0:
                mins = diff.seconds // 60
                return f"{mins}m ago" if mins > 0 else "Just now"
            return f"{hours}h ago"
        elif diff.days == 1:
            return "1d ago"
        elif diff.days < 30:
            return f"{diff.days}d ago"
        return self.posted_at.strftime('%Y-%m-%d')
