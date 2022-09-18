import phonenumbers
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from django.utils.translation import ugettext_lazy as _
from f_hlis.custom_auth.models import ApplicationUser


class CheckUserDataSerializer(ModelSerializer):
    phone = PhoneNumberField()
    country_code = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationUser
        fields = ('email', 'phone', 'password', 'country_code', 'phone_number')

        extra_kwargs = {
            'password': {'required': True, 'validators': [validate_password]},
            'email': {'required': True},
        }

    def get_country_code(self, ojb):
        try:
            phone = phonenumbers.parse(str(ojb['phone']))
            return f'+{phone.country_code}'
        except phonenumbers.NumberParseException:
            return None

    def get_phone_number(self, obj):
        try:
            phone = phonenumbers.parse(str(obj['phone']))
            return str(phone.national_number)
        except phonenumbers.NumberParseException:
            return None


class RegistrationSerializer(ModelSerializer):
    phone = PhoneNumberField(required=True)

    class Meta:
        model = ApplicationUser
        fields = ('first_name', 'last_name', 'phone', 'username', 'country', 'email', 'uuid', 'password',)
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'validators': [validate_password]},
            'email': {'required': True},

        }
        read_only_fields = ('uuid', )

    # def validate(self, attrs):
    #     validated_data = super().validate(attrs)
    #     if not validated_data['password'] == validated_data['confirm_password']:
    #         raise ValidationError(_('Your password is not match!!'))
    #
    #     return validated_data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)

        user.set_password(password)
        user.save(update_fields=['password'])

        return user


class CheckPhoneSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)


class CheckCodeSerializer(serializers.Serializer):
    OTP = serializers.CharField(required=True, max_length=6)