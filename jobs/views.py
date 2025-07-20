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
from rest_framework import generics, permissions
from .models import Job
from .serializers import JobSerializer
from users.models import CustomUser
from django.shortcuts import get_object_or_404

class JobsByUserView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]  # Use IsAuthenticated if needed

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CustomUser, id=user_id)
        return Job.objects.filter(user=user).order_by('-created_at')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Job
from django.shortcuts import get_object_or_404

class JobInterestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        if request.user in job.interested_users.all():
            job.interested_users.remove(request.user)
            return Response({"message": "Interest removed"}, status=status.HTTP_200_OK)
        else:
            job.interested_users.add(request.user)
            return Response({"message": "Interest shown"}, status=status.HTTP_201_CREATED)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Job

class JobApplicantStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        total_applicants = job.interested_users.count()
        return Response({"job_id": job_id, "applicants_count": total_applicants})

class JobSearchView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Job.objects.filter(title__icontains=query).order_by('-created_at')
