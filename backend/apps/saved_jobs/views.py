from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import SavedJob
from .serializers import SavedJobSerializer
from apps.jobs.models import Job
from apps.jobs.serializers import JobSerializer

class SavedJobListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SavedJobSerializer
    pagination_class = None

    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user).select_related('job', 'job__company')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Return job objects with saved=True for seamless frontend rendering
        jobs = [saved.job for saved in queryset]
        serializer = JobSerializer(jobs, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        job_id = request.data.get('job_id') or request.data.get('job')
        if not job_id:
            return Response({'error': 'job_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

        saved, created = SavedJob.objects.get_or_create(user=request.user, job=job)
        return Response({
            'success': True,
            'message': 'Job bookmarked successfully',
            'saved': True,
            'job': JobSerializer(job, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)

class SavedJobDeleteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, job_id):
        deleted_count, _ = SavedJob.objects.filter(
            user=request.user,
            job_id=job_id
        ).delete()

        if deleted_count == 0:
            # Also try pk lookup
            SavedJob.objects.filter(user=request.user, id=job_id).delete()

        return Response({
            'success': True,
            'message': 'Job removed from saved list'
        }, status=status.HTTP_200_OK)
