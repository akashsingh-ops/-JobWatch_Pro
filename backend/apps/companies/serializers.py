from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    job_count = serializers.IntegerField(source='jobs.count', read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'slug', 'description', 'website', 'logo_url', 'industry', 'location', 'job_count', 'created_at']
