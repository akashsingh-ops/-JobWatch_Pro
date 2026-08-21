from rest_framework import serializers
from .models import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(source='created_at', read_only=True)
    type = serializers.CharField(source='event_type')

    class Meta:
        model = ActivityLog
        fields = ['id', 'type', 'event_type', 'action', 'description', 'timestamp', 'created_at', 'metadata']
        read_only_fields = ['id', 'timestamp', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        event_type = validated_data.pop('event_type', None) or validated_data.pop('type', 'data')
        return ActivityLog.objects.create(
            user=user,
            event_type=event_type,
            **validated_data
        )
