from rest_framework import serializers
from .models import Profile
from apps.skills.models import Skill
from apps.skills.serializers import SkillSerializer

class ProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    skills_data = SkillSerializer(source='skills', many=True, read_only=True)
    skill_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Profile
        fields = [
            'id', 'user_email', 'user_name', 'headline', 'bio', 'location',
            'experience_years', 'preferred_roles', 'preferred_locations',
            'salary_expectation', 'remote_preference', 'skills_data', 'skill_names',
            'resume', 'created_at', 'updated_at'
        ]

    def update(self, instance, validated_data):
        skill_names = validated_data.pop('skill_names', None)
        profile = super().update(instance, validated_data)

        if skill_names is not None:
            skill_objs = []
            for name in skill_names:
                name_clean = name.strip()
                if name_clean:
                    skill, _ = Skill.objects.get_or_create(
                        name=name_clean,
                        defaults={'normalized_name': name_clean.lower()}
                    )
                    skill_objs.append(skill)
            profile.skills.set(skill_objs)

        return profile
