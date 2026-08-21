from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'employment_type', 'experience_level', 'location', 'is_active', 'posted_at')
    list_filter = ('category', 'employment_type', 'experience_level', 'remote_type', 'is_active', 'featured')
    search_fields = ('title', 'company__name', 'description', 'location')
    filter_horizontal = ('required_skills',)
    ordering = ('-posted_at',)
