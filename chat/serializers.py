# chat/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ChatMessage
from users.serializers import UserSerializer

User = get_user_model()

class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatMessage model.
    - `sender` and `receiver` are nested read-only representations (UserSerializer).
    - `receiver_id` is a write-only PK field clients can send when creating a message.
    - `timestamp` is read-only (your model uses `timestamp`).
    """
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    # Write-only field to accept a receiver primary key on create
    receiver_id = serializers.PrimaryKeyRelatedField(
        source='receiver',
        queryset=User.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = ChatMessage
        fields = [
            'id',
            'message',
            'sender',
            'receiver',
            'receiver_id',  # allowed on write, not returned in nested form
            'timestamp',
        ]
        read_only_fields = ['id', 'sender', 'receiver', 'timestamp']
