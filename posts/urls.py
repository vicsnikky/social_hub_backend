from django.urls import path
from .views import (
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
    PostAuthorAvatarView,
    PostsByUserView,
    PostSearchView,
    PostLikeToggleView,
    CommentListCreateView,
    CommentRetrieveDestroyView,
    CommentLikeToggleView
)

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('<int:pk>/author-avatar/', PostAuthorAvatarView.as_view(), name='post-author-avatar'),
    path('user/<int:user_id>/', PostsByUserView.as_view(), name='posts-by-user'),
    path('search/', PostSearchView.as_view(), name='post-search'),

    # Likes for post
    path('<int:pk>/like/', PostLikeToggleView.as_view(), name='post-like'),

    # Comments
    path('<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveDestroyView.as_view(), name='comment-detail'),

    # Likes for comments
    path('comments/<int:pk>/like/', CommentLikeToggleView.as_view(), name='comment-like'),
]
