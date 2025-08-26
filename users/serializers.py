from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar",
        ]

    def get_avatar(self, obj):
        request = self.context.get("request")
        if hasattr(obj, "profile_pic") and obj.profile_pic:
            return request.build_absolute_uri(obj.profile_pic.url) if request else obj.profile_pic.url
        return None


# ✅ Signup serializer
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])  # 🔑 hash password
        return super().create(validated_data)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email found.")
        return value

    def save(self, **kwargs):
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]
        user = User.objects.get(email=email)
        user.password = make_password(new_password)  # hash reset password
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        help_text="Enter either your username OR email",
        required=True
    )
    password = serializers.CharField(write_only=True, required=True)
