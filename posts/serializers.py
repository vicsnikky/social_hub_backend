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
        """
        Return the queryset of Like objects for a Post regardless of whether
        the reverse name is `likes` or the default `like_set`.
        """
        if hasattr(obj, "likes"):
            qs = obj.likes.all()
        else:
            qs = obj.like_set.all()
        return qs

    def get_likes_count(self, obj):
        return self._get_like_queryset(obj).count()

    def get_liked_by_users(self, obj):
        likes_qs = self._get_like_queryset(obj)
        users = [l.user for l in likes_qs.select_related("user")]
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
        # Comment model uses a ManyToManyField named `liked_by`
        return obj.liked_by.count()

    def get_liked_by_users(self, obj):
        users_qs = obj.liked_by.all()
        return UserSerializer(users_qs, many=True, context=self.context).data
