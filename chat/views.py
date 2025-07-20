from rest_framework import generics, permissions
from django.db import models
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from django.shortcuts import get_object_or_404
from users.models import CustomUser

class ChatListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        other_id = self.kwargs['user_id']
        user = self.request.user
        other_user = get_object_or_404(CustomUser, id=other_id)
        return ChatMessage.objects.filter(
            models.Q(sender=user, receiver=other_user) |
            models.Q(sender=other_user, receiver=user)
        )

class ChatCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
