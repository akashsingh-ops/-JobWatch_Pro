from django.urls import path
from .views import NotificationListView, NotificationMarkReadView, NotificationDeleteView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification_list'),
    path('read-all/', NotificationMarkReadView.as_view(), name='notification_read_all'),
    path('<int:pk>/read/', NotificationMarkReadView.as_view(), name='notification_read_single'),
    path('clear-all/', NotificationDeleteView.as_view(), name='notification_clear_all'),
    path('<int:pk>/', NotificationDeleteView.as_view(), name='notification_delete'),
]
