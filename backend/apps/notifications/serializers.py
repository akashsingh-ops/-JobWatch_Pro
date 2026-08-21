from rest_framework import serializers
from .models import Notification, AlertPreference

class NotificationSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    read = serializers.BooleanField(source='is_read')
    type = serializers.CharField(source='notification_type')

    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'category', 'type', 'read', 'is_read', 'notification_type', 'metadata', 'date', 'created_at']

    def get_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

class AlertPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertPreference
        fields = [
            'id', 'email_notifications', 'instant_alerts', 'daily_digest',
            'monitored_categories', 'monitored_keywords', 'min_salary',
            'remote_only', 'created_at', 'updated_at'
        ]
