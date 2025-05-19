from django.urls import path
from .views import JobListCreateView, JobRetrieveDestroyView

urlpatterns = [
    path('', JobListCreateView.as_view(), name='job-list-create'),
    path('<int:pk>/', JobRetrieveDestroyView.as_view(), name='job-detail'),
]
