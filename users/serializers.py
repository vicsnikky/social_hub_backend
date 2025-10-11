# users/serializers.py
from django.contrib.auth import get_user_model, authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "profile_pic",
            "avatar",
            "password",
        ]
        read_only_fields = ["id", "avatar"]

    def get_avatar(self, obj):
        request = self.context.get("request")
        pic = getattr(obj, "profile_pic", None)
        if not pic:
            return None
        url = getattr(pic, "url", None)
        if not url:
            return None
        if request:
            return request.build_absolute_uri(url)
        return url

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, help_text="username or email")
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        # Let the view handle whether username is email or username string.
        user = authenticate(username=username, password=password)
        if user is None:
            # Try finding by email if authenticate with username failed (some setups)
            try:
                user_obj = User.objects.get(email=username)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials")
            user = authenticate(username=user_obj.username, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email.")
        return value

    def save(self, **kwargs):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        from django.conf import settings
        frontend = getattr(settings, "FRONTEND_BASE_URL", "http://localhost:3000")
        reset_link = f"{frontend}/reset-password/{uid}/{token}"
        # In production send email with reset_link
        return {"reset_link": reset_link, "uid": uid, "token": token}


class PasswordResetSerializer(serializers.Serializer):
    # token-less reset (email + new_password)
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email.")
        return value

    def save(self, **kwargs):
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return user


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        try:
            uid_decoded = urlsafe_base64_decode(data["uid"]).decode()
            user = User.objects.get(pk=uid_decoded)
        except Exception:
            raise serializers.ValidationError("Invalid UID")

        if not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError("Invalid or expired token")

        user.set_password(data["new_password"])
        user.save()
        return user
