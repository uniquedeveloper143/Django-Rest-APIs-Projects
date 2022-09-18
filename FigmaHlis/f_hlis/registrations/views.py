import random

from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from unicef_restlib.views import MultiSerializerViewSetMixin
from rest_framework.status import HTTP_400_BAD_REQUEST
from f_hlis.custom_auth.models import ApplicationUser
from f_hlis.registrations.serializers import RegistrationSerializer, CheckUserDataSerializer, CheckCodeSerializer, \
    CheckPhoneSerializer
from django.utils.translation import ugettext_lazy as _
import random

rand_code = str(random.randrange(1000, 9999))
code = {"OTP": rand_code}


class RegistrationViewSet(
    MultiSerializerViewSetMixin,
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = ApplicationUser.objects.all().order_by('-first_name')
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)
    serializer_action_classes = {
        'check_user_data': CheckUserDataSerializer,
        'send_sms': CheckPhoneSerializer,
        'check_sms': CheckCodeSerializer,
    }

    @action(methods=['post'], permission_classes=(AllowAny,), detail=False, url_path='check')
    def check_user_data(self, *args, **kwargs):

        if not self.request.data['password'] == self.request.data['confirm_password']:
            raise ValidationError(_('Your password is not match!!'))

        serializer = self.get_serializer(data=self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    @action(methods=['post'], permission_classes=[AllowAny], detail=False, url_path='send_sms')
    def send_sms(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        return Response((serializer.data, code))

    @action(methods=['post'], permission_classes=[AllowAny], detail=False, url_path='check_sms')
    def check_sms(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        if serializer.data != code:
            raise ValidationError('Your code is not match!!')

        return Response("Verified successfully!!")
