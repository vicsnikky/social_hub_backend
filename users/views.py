from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from .serializers import UserSerializer, LoginSerializer 


from .models import CustomUser, UserFollow
from .serializers import UserSerializer, PasswordResetSerializer

User = get_user_model()

# Retrieve all users
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Signup
from .serializers import UserSerializer, UserSignupSerializer, LoginSerializer, PasswordResetSerializer  

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

# Login
class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer   # 👈 use the new serializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username_or_email = request.data.get("username")
        password = request.data.get("password")

        if not username_or_email or not password:
            return Response(
                {"error": "Username/Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        })


# View Profile
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Update Profile
class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Retrieve user by ID
class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Follow / Unfollow
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

# Password Reset (No Token)
class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer

class AllUsersListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # or IsAuthenticated if you want to restrict
