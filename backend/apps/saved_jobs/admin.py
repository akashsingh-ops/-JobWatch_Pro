from django.contrib import admin
from .models import SavedJob

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'created_at')
    search_fields = ('user__email', 'job__title', 'job__company__name')
