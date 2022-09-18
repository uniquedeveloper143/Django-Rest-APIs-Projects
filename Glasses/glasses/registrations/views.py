from random import randrange

from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet
from unicef_restlib.views import MultiSerializerViewSetMixin
from glasses.custom_auth.models import ApplicationUser
from glasses.registrations.serializers import RegistrationSerializer, CheckUserDataSerializer,CheckCodeSerializer,CheckPhoneSerializer

rand_num = str(randrange(1000, 9999))
code = {"OTP": rand_num}
# code = {"OTP": "1234"}


class RegistrationViewSet(
    MultiSerializerViewSetMixin,
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
):
    queryset = ApplicationUser.objects.all().order_by('-date_of_birth')
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    serializer_action_classes = {
        'check_user_data': CheckUserDataSerializer,
        'send_sms': CheckPhoneSerializer,
        'check_sms': CheckCodeSerializer,
    }

    @action(methods=['post'], permission_classes=(AllowAny,), url_name='check',
            url_path='check', detail=False)
    def check_user_data(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    @action(permission_classes=(AllowAny,), methods=['post'], url_name='send_sms_code',
            url_path='send_sms_code', detail=False)
    def send_sms(self, *args, **kwargs):

        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        return Response((serializer.data, code))

    @action(methods=['post'], permission_classes=(AllowAny,), url_path='check_sms_code', url_name='check_sms_code', detail=False)
    def check_sms(self, *args, **kwargs):

        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        if serializer.data!=code:
            raise ValidationError('Not Verified Please enter correct code!!')
        return Response("Verified~!!")
