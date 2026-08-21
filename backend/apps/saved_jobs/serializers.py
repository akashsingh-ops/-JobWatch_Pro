from rest_framework import serializers
from .models import SavedJob
from apps.jobs.serializers import JobSerializer

class SavedJobSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True)

    class Meta:
        model = SavedJob
        fields = ['id', 'user', 'job', 'job_details', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        job = validated_data['job']
        saved_job, _ = SavedJob.objects.get_or_create(user=user, job=job)
        return saved_job
