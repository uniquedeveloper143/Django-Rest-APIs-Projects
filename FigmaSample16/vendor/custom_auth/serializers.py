from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=128)


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if 'username' not in validated_data:
            if 'email' not in validated_data and 'phone' not in validated_data:
                raise ValidationError(_('Username, email or phone should ve provided'))

        return validated_data


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'uuid', 'name', 'email', 'phone',  'user_type', 'password', 'longitude', 'latitude')
        read_only_fields = ('uuid',)

    def create(self, validated_data):
        user = self.get_user()
        validated_data['user'] = user

        return super().create(validated_data)

    def save(self, **kwargs):
        password = self.validated_data.pop('password', None)

        user = super().save(**kwargs)

        # password assignment
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])

        return user
