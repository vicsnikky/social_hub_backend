from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Event
from .serializers import EventSerializer
from rest_framework.response import Response

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-start_time')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EventRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        if event.created_by != request.user:
            return Response({'error': 'You can only delete your own event.'}, status=403)
        return super().delete(request, *args, **kwargs)
