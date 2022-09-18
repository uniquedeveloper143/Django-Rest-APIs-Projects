import phonenumbers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from django.utils.translation import ugettext as _
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError
from unicef_restlib.serializers import UserContextSerializerMixin

from ecommerce.attachments.models import Attachment
# from ecommerce.utils.serializers import ReadOnlySerializerMixin
from ecommerce.custom_auth.models import Address
from ecommerce.order_place.models import Order

User = get_user_model()


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=1020)


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


class UserPhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(source='photo', allow_null=True)
    width = serializers.ReadOnlyField(source='width_photo', allow_null=True)
    height = serializers.ReadOnlyField(source='height_photo', allow_null=True)

    class Meta:
        # model = get_user_model()
        model = User
        fields = ('id', 'image', 'width', 'height')


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'file', 'added_at')
        read_only_fields = fields


class BaseUserSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    attachments = AttachmentSerializer(read_only=True, many=True)
    country_code = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    total_order = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'uuid', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'about', 'photo', 'user_type',
                  'gender', 'password', 'attachments', 'country_code', 'phone_number', 'total_order', )
        read_only_fields = ('uuid',)

    def get_photo(self, obj):
        photo = obj.photo
        if not photo:
            return None
        return UserPhotoSerializer(obj).data

    def get_total_order(self, obj):
        try:
            return Order.objects.filter(user=obj).count()
        except :
            return None

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


class PasswordValidationSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate_password(self, password):
        try:
            validate_password(password)

        except DjangoValidationError as ex:
            raise ValidationError(ex.messages)
        return password


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if validated_data['old_password'] == validated_data['new_password']:
            raise ValidationError(_('Don\'t use the same password! For security reasons, please use a different '
                                    'password to your old one'))
        elif not self.context['request'].user.check_password(validated_data['old_password']):
            raise ValidationError(_('You\'ve entered incorrect old password, please try again. '))

        return validated_data


class UserStatisticSerializerMixin:
    filters_amount = serializers.ReadOnlyField()

    class Meta:
        fields = ('filters_amount', )

 
class AddressSerializer(
    UserContextSerializerMixin,
    serializers.ModelSerializer
):
    user = BaseUserSerializer(read_only=True)
    country_code = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ('id', 'user', 'name', 'phone', 'street_address', 'street_address_two', 'city', 'state', 'zipcode',
                  'latitude', 'longitude', 'country_code', 'phone_number',)

        extra_kwargs = {
            'name': {'required': True},
            'phone': {'required': True},
            'street_address': {'required': True},
            'street_address_two': {'required': True},
            'city': {'required': True},
            'state': {'required': True},
            'zipcode': {'required': True},
            'latitude': {'required': True},
            'longitude': {'required': True},
        }

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
