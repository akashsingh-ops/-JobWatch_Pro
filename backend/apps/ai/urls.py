from django.urls import path
from .views import JobMatchView, ResumeParseView, RecommendationsView

urlpatterns = [
    path('match/<str:job_id>/', JobMatchView.as_view(), name='ai_job_match'),
    path('parse-resume/', ResumeParseView.as_view(), name='ai_parse_resume'),
    path('recommendations/', RecommendationsView.as_view(), name='ai_recommendations'),
]
