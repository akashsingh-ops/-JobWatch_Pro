from rest_framework import views, permissions, status
from rest_framework.response import Response
from apps.jobs.models import Job
from apps.profiles.models import Profile
from apps.jobs.serializers import JobSerializer
from .services.matching import JobMatchingEngine
from .services.resume_parser import ResumeParserService
from .services.job_analyzer import JobAnalyzerService
from .services.recommendations import AIRecommendationService

class JobMatchView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

        profile, _ = Profile.objects.get_or_create(user=request.user)
        match_result = JobMatchingEngine.calculate_match(profile, job)
        analysis = JobAnalyzerService.analyze_job(job)

        return Response({
            'success': True,
            'job_id': job_id,
            'match': match_result,
            'analysis': analysis
        })

class ResumeParseView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        resume_text = request.data.get('resume_text', '')
        parsed = ResumeParserService.parse_resume(resume_text)
        return Response({
            'success': True,
            'parsed': parsed
        })

class RecommendationsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        jobs = AIRecommendationService.get_recommendations(profile)
        serializer = JobSerializer(jobs, many=True, context={'request': request})
        return Response({
            'success': True,
            'recommendations': serializer.data
        })
