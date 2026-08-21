from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'location', 'experience_years', 'remote_preference', 'updated_at')
    search_fields = ('user__email', 'user__name', 'headline', 'location')
    filter_horizontal = ('skills',)
