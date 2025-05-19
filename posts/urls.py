from django.urls import path
from .views import PostListCreateView, PostRetrieveDestroyView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostRetrieveDestroyView.as_view(), name='post-detail'),
]


from .views import like_post

urlpatterns += [
    path('<int:pk>/like/', like_post, name='post-like'),
]


from .views import CommentListCreateView, CommentDeleteView

urlpatterns += [
    path('<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
]
