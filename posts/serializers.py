# posts/serializers.py
from rest_framework import serializers
from django.conf import settings
from .models import Post, Comment, Like
from users.serializers import UserSerializer  # assuming exists

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_avatar = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(source='like_set.count', read_only=True)  # uses Like model
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_avatar', 'content', 'media',
            'likes_count', 'created_at'
        ]

    def get_author_avatar(self, obj):
        request = self.context.get('request')
        avatar = getattr(obj.author, 'profile_pic', None)
        if not avatar:
            return None
        try:
            url = avatar.url
        except Exception:
            return None
        if request:
            return request.build_absolute_uri(url)
        return url

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='liked_by.count', read_only=True)  # if using ManyToManyField
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'likes_count', 'created_at']
        read_only_fields = ['user', 'likes_count', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
