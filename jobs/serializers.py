from rest_framework import serializers
from .models import Job
from users.serializers import UserSerializer


class JobSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # full user with avatar

    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'company_name',
            'location',
            'description',
            'salary_range',
            'deadline',
            'created_by',
            'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']
