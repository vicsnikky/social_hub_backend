from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer
from .serializers import PasswordResetRequestSerializer

User = get_user_model()

# Signup View
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

#  Login View (JWT)
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.data['username'])
            if user.check_password(request.data['password']):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#  View Profile
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Update Profile (bio, profile_pic)
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import CustomUser, UserFollow
from .serializers import UserSerializer

# List all users
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Retrieve user by ID
class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Follow/Unfollow user
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        target = get_object_or_404(CustomUser, id=id)
        if request.user == target:
            return Response({"error": "You cannot follow yourself."}, status=400)

        follow, created = UserFollow.objects.get_or_create(
            follower=request.user,
            following=target
        )
        if not created:
            follow.delete()
            return Response({"message": "Unfollowed"}, status=200)
        return Response({"message": "Followed"}, status=201)

# Followers list
class FollowersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(CustomUser, id=self.kwargs['id'])
        return [f.follower for f in user.followers_set.all()]

# Following list
class FollowingListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(CustomUser, id=self.kwargs['id'])
        return [f.following for f in user.following_set.all()]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RequestPasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset link sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from .serializers import PasswordResetConfirmSerializer

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
