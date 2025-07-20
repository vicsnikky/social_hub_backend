from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Event
from .serializers import EventSerializer
from users.models import CustomUser


# ✅ Create and List Events
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-start_time')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ✅ Retrieve and Delete Event
class EventRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        if event.created_by != request.user:
            return Response({'error': 'You can only delete your own event.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)


# ✅ Get Events by User ID
class EventsByUserView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]  # Or IsAuthenticated if needed

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CustomUser, id=user_id)
        return Event.objects.filter(created_by=user).order_by('-created_at')


# ✅ Toggle Event Interest
class EventInterestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if request.user in event.interested_users.all():
            event.interested_users.remove(request.user)
            return Response({"message": "Interest removed"}, status=status.HTTP_200_OK)
        else:
            event.interested_users.add(request.user)
            return Response({"message": "Interest shown"}, status=status.HTTP_201_CREATED)

class EventAttendeeStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        total_attendees = event.interested_users.count()
        return Response({"event_id": event_id, "attendees_count": total_attendees})

from users.serializers import UserSerializer  # To serialize attendee data

class EventAttendeesListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        event = get_object_or_404(Event, id=event_id)
        return event.interested_users.all()
class EventSearchView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Event.objects.filter(title__icontains=query).order_by('-created_at')
