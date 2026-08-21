from rest_framework import serializers
from .models import Application
from apps.jobs.serializers import JobSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True)
    job_id = serializers.CharField(write_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'user', 'job', 'job_id', 'job_details',
            'status', 'applied_at', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'job', 'created_at', 'updated_at']

    def create(self, validated_data):
        job_id = validated_data.pop('job_id')
        user = self.context['request'].user
        from apps.jobs.models import Job
        job = Job.objects.get(id=job_id)
        
        application, created = Application.objects.update_or_create(
            user=user,
            job=job,
            defaults=validated_data
        )
        return application
