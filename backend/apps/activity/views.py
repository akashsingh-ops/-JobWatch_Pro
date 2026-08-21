from rest_framework import generics, permissions, filters, views
from rest_framework.response import Response
from .models import ActivityLog
from .serializers import ActivityLogSerializer

class ActivityLogListView(generics.ListCreateAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['action', 'description', 'event_type']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        queryset = ActivityLog.objects.all()
        if user.is_authenticated:
            queryset = queryset.filter(user=user)
        
        event_type = self.request.query_params.get('type')
        if event_type and event_type != 'all':
            queryset = queryset.filter(event_type=event_type)
        return queryset[:50]

class ActivityStatsView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        qs = ActivityLog.objects.all()
        if user:
            qs = qs.filter(user=user)

        total_actions = qs.count()
        total_searches = qs.filter(event_type='data').count()
        total_alerts = qs.filter(event_type='alerts').count()
        total_profile_updates = qs.filter(event_type='profile').count()

        return Response({
            'total_actions': total_actions,
            'total_searches': total_searches,
            'total_alerts': total_alerts,
            'total_profile_updates': total_profile_updates,
        })
