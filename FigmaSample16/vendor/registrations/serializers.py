from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from vendor.custom_auth.models import ApplicationUser


class CheckUserDataSerializer(ModelSerializer):
    phone = PhoneNumberField()

    class Meta:
        model = ApplicationUser
        fields = ('email', 'phone', 'password')

        extra_kwargs = {
            'password': {'required': True, 'validators': [validate_password]},
            'email': {'required': True},
        }


class RegistrationSerializer(ModelSerializer):
    phone = PhoneNumberField()

    class Meta:
        model = ApplicationUser
        fields = ('id', 'name', 'email', 'phone', 'password', 'uuid', 'user_type', 'check_agree')
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'email': {'required': True},
            'check_agree': {'required': True},

        }
        read_only_fields = ('uuid',)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        data = validated_data['phone']
        check = validated_data['check_agree']
        phone = ApplicationUser.objects.filter(phone=data)
        if phone:
            raise ValidationError("Phone number already exists.")
        print('check', check)

        if not check:
            raise ValidationError("Please check term and conditions!!")

        return validated_data

    def create(self, validated_data):

        password = validated_data.pop('password', None)
        user = super().create(validated_data)

        user.set_password(password)
        user.save(update_fields=['password'])

        return user


class CheckPhoneSerializer(Serializer):
    phone = PhoneNumberField(required=True)


class CheckCodeSerializer(Serializer):
    OTP = serializers.CharField(required=True)


class ResetPasswordSerializer(Serializer):
    password = serializers.CharField(required=True)
