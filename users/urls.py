from django.urls import path
from .views import (
    UserSignupView,
    UserLoginView,
    UserProfileView,
    UserProfileUpdateView,
    UserListView, 
    UserDetailView,
    FollowUserView, 
    FollowersListView, 
    FollowingListView,
    PasswordResetView,
    AllUsersListView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),

    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    path('<int:id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('<int:id>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('<int:id>/following/', FollowingListView.as_view(), name='following-list'),

    path('forgot-password/', PasswordResetView.as_view(), name='forgot_password'),
    path('all/', AllUsersListView.as_view(), name='all-users'),
]
