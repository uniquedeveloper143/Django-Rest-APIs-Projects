import phonenumbers
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext as _


User = get_user_model()


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=256)


class UserAuthSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        # if 'username' not in validated_data:
        if 'email' not in validated_data and 'phone' not in validated_data:
            raise ValidationError(_('Email and phone should be provided'))

        return validated_data


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    country_code = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'uuid', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'about', 'user_type',
                  'gender', 'password', 'country_code', 'phone_number', )
        read_only_fields = ('uuid',)

    def get_country_code(self, obj):
        try:
            phone = phonenumbers.parse(str(obj.phone))
            return f'+{phone.country_code}'
        except phonenumbers.NumberParseException:
            return None

    def create(self, validated_data):
        user = self.get_user()
        validated_data['user'] = user

        return super().create(validated_data)

    def get_phone_number(self, obj):
        try:
            phone = phonenumbers.parse(str(obj.phone))
            return str(phone.national_number)
        except phonenumbers.NumberParseException:
            return None

    def save(self, **kwargs):
        password = self.validated_data.pop('password', None)

        user = super().save(**kwargs)

        # password assignment
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])

        return user
