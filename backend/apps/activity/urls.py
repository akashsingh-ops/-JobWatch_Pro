from django.urls import path
from .views import ActivityLogListView, ActivityStatsView

urlpatterns = [
    path('', ActivityLogListView.as_view(), name='activity_list_create'),
    path('stats/', ActivityStatsView.as_view(), name='activity_stats'),
]
