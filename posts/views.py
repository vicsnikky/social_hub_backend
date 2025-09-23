# posts/views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from users.models import CustomUser


# ---------- Helpers ----------
def _user_avatar_url(request, user):
    """
    Return absolute avatar URL for a user or None.
    Uses `profile_pic` (your CustomUser field).
    """
    pic = getattr(user, "profile_pic", None)
    if pic:
        try:
            return request.build_absolute_uri(pic.url)
        except Exception:
            # fallback to relative url if build_absolute_uri fails
            return getattr(pic, "url", None)
    return None


def _post_like_queryset(post):
    """
    Return an iterable of (user) who liked the post, and the mechanism used:
    - if Post has M2M 'liked_by' -> use that
    - else use Like model (reverse name 'likes' or 'like_set')
    Returns tuple (users_iterable, 'm2m'|'like_model')
    """
    if hasattr(post, "liked_by"):
        return (post.liked_by.all(), "m2m")

    # fallback to Like model
    # check for related_name 'likes' or default like_set
    if hasattr(post, "likes"):
        likes_qs = post.likes.select_related("user").all()
    else:
        likes_qs = getattr(post, "like_set", Like.objects.filter(post=post)).select_related("user")
    users = [lk.user for lk in likes_qs]
    return (users, "like_model")


# ---------- Posts ----------

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update({"request": self.request})
        return ctx


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied("You can only edit your own post.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own post.")
        instance.delete()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update({"request": self.request})
        return ctx


# ---------- Post like/unlike & GET likes ----------

class PostLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        # If Post uses M2M liked_by
        if hasattr(post, "liked_by"):
            if request.user in post.liked_by.all():
                post.liked_by.remove(request.user)
                return Response({"message": "Post unliked."}, status=status.HTTP_200_OK)
            post.liked_by.add(request.user)
            return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)

        # Otherwise use Like model
        like_qs = Like.objects.filter(user=request.user, post=post)
        if like_qs.exists():
            like_qs.delete()
            return Response({"message": "Post unliked."}, status=status.HTTP_200_OK)
        # create
        Like.objects.create(user=request.user, post=post)
        return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        users_or_iter, mechanism = _post_like_queryset(post)

        # users_or_iter might already be list/queryset of users
        # build minimal user representation with avatar
        users_data = []
        for u in users_or_iter:
            users_data.append(
                {
                    "id": u.id,
                    "username": u.username,
                    "avatar": _user_avatar_url(request, u),
                }
            )

        return Response({"count": len(users_data), "likes": users_data}, status=status.HTTP_200_OK)


# ---------- Comments ----------

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        serializer.save(user=self.request.user, post_id=post_id)


class CommentRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own comment.")
        instance.delete()


class CommentLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        # Comment model uses M2M named liked_by (per your model)
        if request.user in comment.liked_by.all():
            comment.liked_by.remove(request.user)
            return Response({"message": "Comment unliked."}, status=status.HTTP_200_OK)
        comment.liked_by.add(request.user)
        return Response({"message": "Comment liked."}, status=status.HTTP_201_CREATED)

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        users_qs = comment.liked_by.all()
        data = [
            {
                "id": u.id,
                "username": u.username,
                "avatar": _user_avatar_url(request, u),
            }
            for u in users_qs
        ]
        return Response({"count": users_qs.count(), "likes": data}, status=status.HTTP_200_OK)


# ---------- Utility endpoints ----------

class PostsByUserView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(CustomUser, id=user_id)
        return Post.objects.filter(author=user).order_by("-created_at")


class PostSearchView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        q = self.request.query_params.get("q", "")
        return Post.objects.filter(content__icontains=q).order_by("-created_at")
