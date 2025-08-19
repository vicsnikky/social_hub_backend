from rest_framework import serializers
from .models import Post, Comment, Like
from users.serializers import UserSerializer  # For showing user details with avatar


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by_users = serializers.SerializerMethodField()

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
        read_only_fields = ['id', 'author', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked_by_users(self, obj):
        users = [like.user for like in obj.likes.all()]
        return UserSerializer(users, many=True, context=self.context).data


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by_users = serializers.SerializerMethodField()

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
        read_only_fields = ['id', 'post', 'user', 'created_at']

    def get_likes_count(self, obj):
        return obj.liked_by.count()

    def get_liked_by_users(self, obj):
        return UserSerializer(obj.liked_by.all(), many=True, context=self.context).data
