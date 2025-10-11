# chat/views.py
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import ChatMessage
from .serializers import ChatMessageSerializer
from users.models import CustomUser

class ChatListView(generics.ListAPIView):
    """
    List messages between the authenticated user and another user (user_id in URL).
    Example: GET /api/chat/<user_id>/
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        other_id = self.kwargs.get('user_id')
        user = self.request.user
        other_user = get_object_or_404(CustomUser, id=other_id)
        return ChatMessage.objects.filter(
            Q(sender=user, receiver=other_user) | Q(sender=other_user, receiver=user)
        ).order_by('timestamp')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update({'request': self.request})
        return ctx


class ChatCreateView(generics.CreateAPIView):
    """
    Create a chat message.
    - Preferred URL: POST /api/chat/<user_id>/send/  (user_id = receiver id)
    - Or POST /api/chat/send/ with body {'receiver_id': <id>, 'message': '...'}
    The authenticated user is set as the sender automatically.
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        request = self.request
        # Try to get receiver from URL kwarg 'user_id'
        receiver = None
        user_id = self.kwargs.get('user_id')
        if user_id:
            receiver = get_object_or_404(CustomUser, id=int(user_id))

        # If receiver not provided via URL, the serializer may have a validated 'receiver'
        validated_receiver = serializer.validated_data.get('receiver') if hasattr(serializer, 'validated_data') else None

        if not receiver and validated_receiver:
            receiver = validated_receiver

        if receiver:
            serializer.save(sender=request.user, receiver=receiver)
        else:
            # Let serializer raise validation error (e.g. receiver_id missing)
            serializer.save(sender=request.user)

    def create(self, request, *args, **kwargs):
        """
        Override to ensure we call serializer.is_valid() prior to perform_create,
        so that `perform_create` can rely on serializer.validated_data if necessary.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # use the same header behavior as CreateAPIView
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
