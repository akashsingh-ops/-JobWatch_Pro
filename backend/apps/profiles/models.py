from django.db import models
from django.conf import settings
from apps.skills.models import Skill

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    headline = models.CharField(max_length=255, blank=True, default='Software Engineer')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True, default='San Francisco, CA')
    experience_years = models.PositiveIntegerField(default=3)
    preferred_roles = models.JSONField(default=list, blank=True)
    preferred_locations = models.JSONField(default=list, blank=True)
    salary_expectation = models.CharField(max_length=100, blank=True, default='$120,000 - $160,000')
    remote_preference = models.CharField(
        max_length=20,
        choices=(('remote', 'Remote'), ('hybrid', 'Hybrid'), ('onsite', 'On-site'), ('any', 'Any')),
        default='any'
    )
    skills = models.ManyToManyField(Skill, related_name='profiles', blank=True)
    resume = models.TextField(blank=True, help_text='Resume text or markdown summary')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.email}"
