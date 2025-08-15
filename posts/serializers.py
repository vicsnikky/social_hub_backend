from rest_framework import serializers
from .models import Post, Comment
from users.serializers import UserSerializer  # To show author and liked_by details


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by_users = UserSerializer(source='liked_by', many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'content',
            'media',
            'created_at',
            'likes_count',
            'liked_by_users'
        ]

    def get_likes_count(self, obj):
        return obj.liked_by.count()


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by_users = UserSerializer(source='liked_by', many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'user',
            'content',
            'created_at',
            'likes_count',
            'liked_by_users'
        ]
        read_only_fields = ['post', 'user', 'created_at']

    def get_likes_count(self, obj):
        return obj.liked_by.count()
