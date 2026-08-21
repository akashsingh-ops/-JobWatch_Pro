import django_filters
from django.db.models import Q
from .models import Job

class JobFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    category = django_filters.CharFilter(lookup_expr='iexact')
    type = django_filters.CharFilter(field_name='employment_type', lookup_expr='iexact')
    employment_type = django_filters.CharFilter(lookup_expr='iexact')
    experienceLevel = django_filters.CharFilter(field_name='experience_level', lookup_expr='iexact')
    experience_level = django_filters.CharFilter(lookup_expr='iexact')
    location = django_filters.CharFilter(lookup_expr='icontains')
    remote_type = django_filters.CharFilter(lookup_expr='iexact')
    company = django_filters.CharFilter(field_name='company__name', lookup_expr='icontains')
    featured = django_filters.BooleanFilter()

    class Meta:
        model = Job
        fields = ['category', 'type', 'employment_type', 'experienceLevel', 'experience_level', 'location', 'remote_type', 'featured']

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(company__name__icontains=value) |
            Q(location__icontains=value) |
            Q(category__icontains=value) |
            Q(required_skills__name__icontains=value)
        ).distinct()
