from django.urls import path
from .views import AlertPreferenceView

urlpatterns = [
    path('', AlertPreferenceView.as_view(), name='alert_preferences'),
]
