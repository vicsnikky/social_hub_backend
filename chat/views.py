from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import models
from django.shortcuts import get_object_or_404
from users.models import CustomUser
from .models import ChatMessage
from .serializers import ChatMessageSerializer


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
        ).order_by("timestamp")


class ChatCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        receiver_id = self.kwargs.get("user_id")  # ✅ expects /chat/<user_id>/send/
        receiver = get_object_or_404(CustomUser, id=receiver_id)
        serializer.save(sender=self.request.user, receiver=receiver)
