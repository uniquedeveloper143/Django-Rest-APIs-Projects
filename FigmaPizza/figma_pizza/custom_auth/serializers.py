from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
User = get_user_model()


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=128)


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if 'email' not in validated_data:
            raise ValidationError("Email is required!")
        return validated_data


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'uuid', 'full_name', 'email', 'password')
        read_only_fields = ('uuid',)

    def create(self, validated_data):
        user = self.get_user()
        validated_data['user'] = user
        return super().create(validated_data)

    def save(self, **kwargs):
        password = self.validated_data.pop('password', None)
        user = super().save(**kwargs)

        if password:
            user.set_password(password)
            user.save(update_fields=['password'])

        return user


class PasswordPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
