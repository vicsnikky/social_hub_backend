from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Job
from .serializers import JobSerializer
from users.models import CustomUser

# ✅ List & Create Jobs
class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# ✅ Retrieve, Update (Edit) & Delete Job
class JobRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        job = self.get_object()
        if job.created_by != self.request.user:
            return Response({'error': 'You can only edit your own job post.'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_destroy(self, instance):
        if instance.created_by != self.request.user:
            return Response({'error': 'You can only delete your own job post.'}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()

# ✅ Get Jobs by User ID
class JobsByUserView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]  # Change to IsAuthenticated if needed

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CustomUser, id=user_id)
        return Job.objects.filter(created_by=user).order_by('-created_at')

# ✅ Show/Remove Interest in Job
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

# ✅ Get Job Applicant Count
class JobApplicantStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        total_applicants = job.interested_users.count()
        return Response({"job_id": job_id, "applicants_count": total_applicants})

# ✅ Search Jobs
class JobSearchView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Job.objects.filter(title__icontains=query).order_by('-created_at')
