from django.contrib.auth.password_validation import validate_password

from rest_framework.serializers import ModelSerializer, Serializer

from phonenumber_field.serializerfields import PhoneNumberField

from blogs.custom_auth.models import ApplicationUser


class CheckPhoneSerializer(Serializer):
    phone = PhoneNumberField(required=True)


class CheckUserDataSerializer(ModelSerializer):
    phone = PhoneNumberField()

    class Meta:
        model = ApplicationUser
        fields = ('email', 'phone', 'password', 'fullname', 'gender', 'date_of_birth', 'city',)
        extra_kwargs = {
            'password': {'validators': [validate_password]},
            'email': {'required': True},
            'fullname': {'required': True},
            'gender': {'required': True},
            'date_of_birth': {'required': True},
            'city': {'required': True},
        }


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = ApplicationUser
        fields = ('fullname', 'email', 'phone', 'password', 'uuid', 'gender', 'date_of_birth', 'city')
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'email': {'required': True},
            'fullname': {'required': True},
            'gender': {'required': True},
            'date_of_birth': {'required': True},
            'city': {'required': True},
        }
        read_only_fields = ('uuid',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)

        # password assigment
        user.set_password(password)
        user.save(update_fields=['password'])

        return user
