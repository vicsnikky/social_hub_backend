from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company_name', 'location',
            'description', 'salary_range', 'deadline',
            'created_by', 'created_by_username', 'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_by_username', 'created_at']
