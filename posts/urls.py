from django.urls import path
from .views import (
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
    PostsByUserView,
    PostSearchView,
    PostLikeToggleView,
    CommentListCreateView,
    CommentRetrieveDestroyView,
    CommentLikeToggleView,
)

urlpatterns = [
    # ✅ Posts
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('user/<int:user_id>/', PostsByUserView.as_view(), name='posts-by-user'),
    path('search/', PostSearchView.as_view(), name='post-search'),

    # ✅ Post likes (toggle + list who liked)
    path('<int:pk>/like/', PostLikeToggleView.as_view(), name='post-like'),

    # ✅ Comments on a post
    path('<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveDestroyView.as_view(), name='comment-detail'),

    # ✅ Comment likes (toggle + list who liked)
    path('comments/<int:pk>/like/', CommentLikeToggleView.as_view(), name='comment-like'),
]
