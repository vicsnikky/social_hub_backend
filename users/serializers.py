# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # show an absolute avatar url in responses
    avatar = serializers.SerializerMethodField(read_only=True)

    # allow password to be written but never returned
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        # include bio & profile_pic so frontend can send them on signup / update
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
        if pic:
            try:
                return request.build_absolute_uri(pic.url) if request else pic.url
            except Exception:
                return getattr(pic, "url", None)
        return None

    def create(self, validated_data):
        # Pop password and create user with proper hashing
        password = validated_data.pop("password", None)
        # If your CustomUser manager supports create_user, use it:
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            # fallback - shouldn't normally happen because password is required
            user.password = make_password(None)
        user.save()
        return user

    def update(self, instance, validated_data):
        # handle password update if provided
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
