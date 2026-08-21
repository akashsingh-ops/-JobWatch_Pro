from rest_framework import serializers
from .models import JobMatchScore

class JobMatchScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobMatchScore
        fields = ['id', 'user', 'job', 'score', 'reasons', 'missing_skills', 'recommendations', 'updated_at']
