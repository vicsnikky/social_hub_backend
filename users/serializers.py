from rest_framework import serializers
from .models import CustomUser, UserFollow

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_pic', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserFollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField()
    following = serializers.StringRelatedField()

    class Meta:
        model = UserFollow
        fields = ['id', 'follower', 'following', 'followed_at']

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist")
        return value

    def save(self):
        user = CustomUser.objects.get(email=self.validated_data['email'])
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_link = f"{settings.FRONTEND_BASE_URL}/reset-password/{uid}/{token}"
        
        # Send email (configure SMTP in production)
        send_mail(
            subject="Reset Your Password",
            message=f"Use the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return reset_link
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from .models import CustomUser


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = urlsafe_base64_decode(data['uid']).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError('Invalid UID')

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError('Invalid or expired token')

        user.set_password(data['new_password'])
        user.save()
        return user
