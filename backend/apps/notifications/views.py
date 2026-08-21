from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Notification, AlertPreference
from .serializers import NotificationSerializer, AlertPreferenceSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class NotificationMarkReadView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk=None):
        if pk:
            Notification.objects.filter(user=request.user, id=pk).update(is_read=True)
        else:
            # Mark all as read
            Notification.objects.filter(user=request.user).update(is_read=True)
        return Response({'success': True, 'message': 'Notification(s) marked as read'})

class NotificationDeleteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk=None):
        if pk:
            Notification.objects.filter(user=request.user, id=pk).delete()
        else:
            Notification.objects.filter(user=request.user).delete()
        return Response({'success': True, 'message': 'Notification(s) cleared'})

class AlertPreferenceView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pref, _ = AlertPreference.objects.get_or_create(user=request.user)
        serializer = AlertPreferenceSerializer(pref)
        return Response({'success': True, 'preferences': serializer.data})

    def patch(self, request):
        pref, _ = AlertPreference.objects.get_or_create(user=request.user)
        serializer = AlertPreferenceSerializer(pref, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'preferences': serializer.data})
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
