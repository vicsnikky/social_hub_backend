from django.urls import path
from .views import EventListCreateView, EventRetrieveDestroyView

urlpatterns = [
    path('', EventListCreateView.as_view(), name='event-list-create'),
    path('<int:pk>/', EventRetrieveDestroyView.as_view(), name='event-detail'),
]
