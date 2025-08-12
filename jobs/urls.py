from django.urls import path
from .views import (
    JobListCreateView,
    JobRetrieveUpdateDestroyView,
    JobsByUserView,
    JobInterestView,
    JobApplicantStatsView,
    JobSearchView
)

urlpatterns = [
    path('', JobListCreateView.as_view(), name='job-list-create'),
    path('<int:pk>/', JobRetrieveUpdateDestroyView.as_view(), name='job-detail'),
    path('user/<int:user_id>/', JobsByUserView.as_view(), name='jobs-by-user'),
    path('<int:job_id>/interest/', JobInterestView.as_view(), name='job-interest'),
    path('<int:job_id>/applicants/stats/', JobApplicantStatsView.as_view(), name='job-applicant-stats'),
    path('search/', JobSearchView.as_view(), name='job-search'),
]
