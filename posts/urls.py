from django.urls import path
from .views import PostListCreateView, PostRetrieveDestroyView, PostsByUserView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostRetrieveDestroyView.as_view(), name='post-detail'),
]


from .views import like_post

urlpatterns += [
    path('<int:pk>/like/', like_post, name='post-like'),
]


from .views import CommentListCreateView, CommentDeleteView, PostSearchView

urlpatterns += [
    path('<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('user/<int:user_id>/', PostsByUserView.as_view(), name='posts-by-user'),
    path('search/', PostSearchView.as_view(), name='post-search'),
]
