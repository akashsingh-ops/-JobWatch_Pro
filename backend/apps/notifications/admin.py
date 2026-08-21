from django.contrib import admin
from .models import Notification, AlertPreference

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'category', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'category')
    search_fields = ('title', 'message', 'user__email')

@admin.register(AlertPreference)
class AlertPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'instant_alerts', 'daily_digest', 'updated_at')
