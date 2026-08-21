from django.urls import path
from .views import SavedJobListCreateView, SavedJobDeleteView

urlpatterns = [
    path('', SavedJobListCreateView.as_view(), name='saved_job_list_create'),
    path('<str:job_id>/', SavedJobDeleteView.as_view(), name='saved_job_delete'),
]
