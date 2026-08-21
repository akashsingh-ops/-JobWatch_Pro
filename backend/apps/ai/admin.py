from django.contrib import admin
from .models import JobMatchScore

@admin.register(JobMatchScore)
class JobMatchScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'score', 'updated_at')
    list_filter = ('score',)
    search_fields = ('user__email', 'job__title')
