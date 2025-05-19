from django.urls import path
from .views import (
    UserSignupView,
    UserLoginView,
    UserProfileView,
    UserProfileUpdateView  
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),  # ✅ Add this
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
