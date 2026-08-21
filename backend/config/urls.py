"""
Root URL Configuration for JobWatch Pro.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1 Versioned endpoints
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/profile/', include('apps.profiles.urls')),
    path('api/v1/skills/', include('apps.skills.urls')),
    path('api/v1/companies/', include('apps.companies.urls')),
    path('api/v1/jobs/', include('apps.jobs.urls')),
    path('api/v1/saved-jobs/', include('apps.saved_jobs.urls')),
    path('api/v1/applications/', include('apps.applications.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/alerts/', include('apps.notifications.urls_alerts')),
    path('api/v1/activity/', include('apps.activity.urls')),
    path('api/v1/ai/', include('apps.ai.urls')),

    # Direct /api/ aliases for ease of consumption
    path('api/auth/', include('apps.accounts.urls')),
    path('api/profile/', include('apps.profiles.urls')),
    path('api/skills/', include('apps.skills.urls')),
    path('api/companies/', include('apps.companies.urls')),
    path('api/jobs/', include('apps.jobs.urls')),
    path('api/saved-jobs/', include('apps.saved_jobs.urls')),
    path('api/applications/', include('apps.applications.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/alerts/', include('apps.notifications.urls_alerts')),
    path('api/activity/', include('apps.activity.urls')),
    path('api/ai/', include('apps.ai.urls')),
]
