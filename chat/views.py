from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import ChatMessage
from .serializers import ChatMessageSerializer
from users.models import CustomUser


class ChatListView(generics.ListAPIView):
    """
    List all chat messages between the authenticated user and another user.
    URL should provide `user_id` (the other user's id).
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        other_id = self.kwargs.get('user_id')
        user = self.request.user
        other_user = get_object_or_404(CustomUser, pk=other_id)
        return ChatMessage.objects.filter(
            Q(sender=user, receiver=other_user) | Q(sender=other_user, receiver=user)
        ).order_by('created_at')


class ChatCreateView(generics.CreateAPIView):
    """
    Create a chat message. Receiver can be passed either in URL as `user_id`
    or in request body as `"receiver": <id>`.
    The view ensures we pass a CustomUser instance to serializer.save(...)
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # prefer URL param first, then body
        receiver_id = self.kwargs.get('user_id') or request.data.get('receiver')
        if receiver_id is None:
            return Response({"error": "Missing receiver id."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure we have an integer id (or convertible string)
        try:
            receiver = get_object_or_404(CustomUser, pk=int(receiver_id))
        except (ValueError, TypeError):
            return Response({"error": "Invalid receiver id."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # pass real CustomUser instance to serializer.save
        serializer.save(sender=self.request.user, receiver=receiver)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
