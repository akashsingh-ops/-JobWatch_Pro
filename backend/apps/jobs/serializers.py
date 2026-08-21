from rest_framework import serializers
from .models import Job
from apps.companies.models import Company
from apps.skills.models import Skill
from apps.skills.serializers import SkillSerializer
from apps.saved_jobs.models import SavedJob

class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_logo = serializers.CharField(source='company.logo_url', read_only=True)
    skills = SkillSerializer(source='required_skills', many=True, read_only=True)
    
    # Frontend compatibility fields
    company = serializers.CharField(source='company.name', read_only=True)
    type = serializers.CharField(source='employment_type', read_only=True)
    experienceLevel = serializers.CharField(source='experience_level', read_only=True)
    postedDate = serializers.SerializerMethodField()
    applyUrl = serializers.CharField(source='application_url', read_only=True)
    saved = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'company',
            'company_name',
            'company_logo',
            'location',
            'type',
            'employment_type',
            'category',
            'remote_type',
            'experienceLevel',
            'experience_level',
            'salary',
            'salary_min',
            'salary_max',
            'salary_currency',
            'description',
            'requirements',
            'skills',
            'applyUrl',
            'application_url',
            'postedDate',
            'posted_at',
            'saved',
            'featured',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def get_postedDate(self, obj):
        return obj.posted_date_formatted

    def get_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedJob.objects.filter(user=request.user, job=obj).exists()
        return False

class JobCreateSerializer(serializers.ModelSerializer):
    company = serializers.CharField(write_only=True, required=True)
    type = serializers.CharField(write_only=True, required=False)
    experienceLevel = serializers.CharField(write_only=True, required=False)
    applyUrl = serializers.URLField(write_only=True, required=False)
    skills = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'location', 'category', 'type', 'employment_type',
            'experienceLevel', 'experience_level', 'salary', 'description', 'requirements',
            'applyUrl', 'application_url', 'remote_type', 'skills', 'featured'
        ]

    def create(self, validated_data):
        company_name = validated_data.pop('company')
        company, _ = Company.objects.get_or_create(
            name=company_name.strip(),
            defaults={'industry': 'Technology'}
        )

        emp_type = validated_data.pop('type', None) or validated_data.get('employment_type', 'Full-time')
        exp_lvl = validated_data.pop('experienceLevel', None) or validated_data.get('experience_level', 'Mid')
        apply_url = validated_data.pop('applyUrl', None) or validated_data.get('application_url', 'https://example.com/apply')
        skill_names = validated_data.pop('skills', [])

        job = Job.objects.create(
            company=company,
            employment_type=emp_type,
            experience_level=exp_lvl,
            application_url=apply_url,
            **validated_data
        )

        if skill_names:
            skill_objs = []
            for name in skill_names:
                name_clean = name.strip()
                if name_clean:
                    skill, _ = Skill.objects.get_or_create(
                        name=name_clean,
                        defaults={'normalized_name': name_clean.lower()}
                    )
                    skill_objs.append(skill)
            job.required_skills.set(skill_objs)

        return job
