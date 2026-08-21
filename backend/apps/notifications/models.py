from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPE_CHOICES = (
        ('job_alert', 'Job Alert'),
        ('application_update', 'Application Update'),
        ('job_closing', 'Job Closing Soon'),
        ('skill_gap', 'Skill Gap'),
        ('ai_recommendation', 'AI Recommendation'),
        ('digest', 'Daily Digest'),
        ('system', 'System'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    category = models.CharField(max_length=100, default='General')
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='job_alert')
    is_read = models.BooleanField(default=False, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} for {self.user.email}"

class AlertPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alert_preferences')
    email_notifications = models.BooleanField(default=True)
    instant_alerts = models.BooleanField(default=True)
    daily_digest = models.BooleanField(default=False)
    monitored_categories = models.JSONField(default=list, blank=True)
    monitored_keywords = models.JSONField(default=list, blank=True)
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    remote_only = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Alert preferences of {self.user.email}"
