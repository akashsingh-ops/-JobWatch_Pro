from django.db import models
from django.conf import settings

class ActivityLog(models.Model):
    EVENT_TYPES = (
        ('profile', 'Profile'),
        ('alerts', 'Alerts'),
        ('data', 'Data / Search'),
        ('settings', 'Settings'),
        ('security', 'Security'),
        ('job_view', 'Job View'),
        ('application', 'Application'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_logs',
        null=True,
        blank=True
    )
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES, default='data', db_index=True)
    action = models.CharField(max_length=150)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        user_str = self.user.email if self.user else "Anonymous"
        return f"{user_str} - {self.action} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
