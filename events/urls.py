from django.urls import path
from .views import EventListCreateView, EventRetrieveDestroyView, EventsByUserView, EventInterestView, EventAttendeeStatsView, EventAttendeesListView, EventSearchView

urlpatterns = [
    path('', EventListCreateView.as_view(), name='event-list-create'),
    path('<int:pk>/', EventRetrieveDestroyView.as_view(), name='event-detail'),
    path('user/<int:user_id>/', EventsByUserView.as_view(), name='events-by-user'),
    path('<int:event_id>/interest/', EventInterestView.as_view(), name='event-interest'),
    path('<int:event_id>/attendees/stats/', EventAttendeeStatsView.as_view(), name='event-attendee-stats'),
    path('<int:event_id>/attendees/', EventAttendeesListView.as_view(), name='event-attendees-list'),
    path('search/', EventSearchView.as_view(), name='event-search'),
]
