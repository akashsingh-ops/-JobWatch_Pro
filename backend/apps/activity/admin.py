from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'event_type', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('action', 'description', 'user__email')
