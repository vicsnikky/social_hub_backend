from rest_framework import serializers
from .models import Event
from users.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # full user with avatar

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'location',
            'start_time',
            'end_time',
            'created_by',
            'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']
