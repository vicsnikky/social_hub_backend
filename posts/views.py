from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from users.models import CustomUser


# ✅ List & Create Posts
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update({'request': self.request})
        return ctx


# ✅ Retrieve, Update, Delete Post
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
        ctx.update({'request': self.request})
        return ctx


# ✅ Like / Unlike Post & Get Likes
class PostLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
            return Response({'message': 'Post unliked.'}, status=status.HTTP_200_OK)
        else:
            post.liked_by.add(request.user)
            return Response({'message': 'Post liked.'}, status=status.HTTP_201_CREATED)

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        likes_qs = post.liked_by.all()
        data = [
            {
                'id': user.id,
                'username': user.username,
                'avatar': request.build_absolute_uri(user.avatar.url) if getattr(user, 'avatar', None) else None
            }
            for user in likes_qs
        ]
        return Response({'count': likes_qs.count(), 'likes': data}, status=status.HTTP_200_OK)


# ✅ Comments: List & Create
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(user=self.request.user, post_id=post_id)


# ✅ Comment: Retrieve & Delete
class CommentRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own comment.")
        instance.delete()


# ✅ Like / Unlike Comment & Get Likes
class CommentLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user in comment.liked_by.all():
            comment.liked_by.remove(request.user)
            return Response({'message': 'Comment unliked.'}, status=status.HTTP_200_OK)
        else:
            comment.liked_by.add(request.user)
            return Response({'message': 'Comment liked.'}, status=status.HTTP_201_CREATED)

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        likes_qs = comment.liked_by.all()
        data = [
            {
                'id': user.id,
                'username': user.username,
                'avatar': request.build_absolute_uri(user.avatar.url) if getattr(user, 'avatar', None) else None
            }
            for user in likes_qs
        ]
        return Response({'count': likes_qs.count(), 'likes': data}, status=status.HTTP_200_OK)


# ✅ Posts by User
class PostsByUserView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CustomUser, id=user_id)
        return Post.objects.filter(author=user).order_by('-created_at')


# ✅ Search Posts
class PostSearchView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        q = self.request.query_params.get('q', '')
        return Post.objects.filter(content__icontains=q).order_by('-created_at')
