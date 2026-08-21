from rest_framework import generics, permissions, filters
from .models import Skill
from .serializers import SkillSerializer

class SkillListView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category']
    ordering_fields = ['name', 'category']
    pagination_class = None  # Return all skills for dropdowns
