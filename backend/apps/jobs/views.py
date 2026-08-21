from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Job
from .serializers import JobSerializer, JobCreateSerializer
from .filters import JobFilter

class StandardJobPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'limit'
    max_page_size = 100

    def get_paginated_response(self, data):
        total_pages = self.page.paginator.num_pages
        return Response({
            'count': self.page.paginator.count,
            'total': self.page.paginator.count,
            'page': self.page.number,
            'totalPages': total_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'jobs': data,  # frontend compatibility
        })

class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.filter(is_active=True).select_related('company').prefetch_related('required_skills')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = JobFilter
    pagination_class = StandardJobPagination
    ordering = ['-posted_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobCreateSerializer
        return JobSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = serializer.save()
        read_serializer = JobSerializer(job, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all().select_related('company').prefetch_related('required_skills')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = JobSerializer
    lookup_field = 'pk'
