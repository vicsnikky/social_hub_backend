from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Job
from .serializers import JobSerializer

class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class JobRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        job = self.get_object()
        if job.created_by != request.user:
            return Response({'error': 'You can only delete your own job post.'}, status=403)
        return super().delete(request, *args, **kwargs)

