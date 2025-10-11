# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Like
from users.serializers import UserSerializer


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "user", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by_users = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "media",
            "created_at",
            "likes_count",
            "liked_by_users",
        ]
        read_only_fields = ["id", "author", "created_at"]

    def _get_like_queryset(self, obj):
        # handles reverse relation whether it's 'likes' or 'like_set'
        if hasattr(obj, "likes"):
            return obj.likes.all()
        return obj.like_set.all()

    def get_likes_count(self, obj):
        return self._get_like_queryset(obj).count()

    def get_liked_by_users(self, obj):
        qs = self._get_like_queryset(obj).select_related("user")
        users = [like.user for like in qs]
        return UserSerializer(users, many=True, context=self.context).data


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by_users = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "user",
            "content",
            "created_at",
            "likes_count",
            "liked_by_users",
        ]
        read_only_fields = ["id", "post", "user", "created_at"]

    def get_likes_count(self, obj):
        # Comment has a ManyToManyField `liked_by`
        return obj.liked_by.count()

    def get_liked_by_users(self, obj):
        users_qs = obj.liked_by.all()
        return UserSerializer(users_qs, many=True, context=self.context).data
# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Like
from users.serializers import UserSerializer


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "user", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by_users = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "media",
            "created_at",
            "likes_count",
            "liked_by_users",
        ]
        read_only_fields = ["id", "author", "created_at"]

    def _get_like_queryset(self, obj):
        # handles reverse relation whether it's 'likes' or 'like_set'
        if hasattr(obj, "likes"):
            return obj.likes.all()
        return obj.like_set.all()

    def get_likes_count(self, obj):
        return self._get_like_queryset(obj).count()

    def get_liked_by_users(self, obj):
        qs = self._get_like_queryset(obj).select_related("user")
        users = [like.user for like in qs]
        return UserSerializer(users, many=True, context=self.context).data


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by_users = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "user",
            "content",
            "created_at",
            "likes_count",
            "liked_by_users",
        ]
        read_only_fields = ["id", "post", "user", "created_at"]

    def get_likes_count(self, obj):
        # Comment has a ManyToManyField `liked_by`
        return obj.liked_by.count()

    def get_liked_by_users(self, obj):
        users_qs = obj.liked_by.all()
        return UserSerializer(users_qs, many=True, context=self.context).data
