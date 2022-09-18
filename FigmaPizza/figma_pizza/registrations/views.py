import random
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from unicef_restlib.views import MultiSerializerViewSetMixin
from figma_pizza.custom_auth.models import ApplicationUser
from figma_pizza.registrations.serializers import RegistrationSerializer, CheckUserDataSerializer, CheckPhoneSerializer, CheckCodeSerializer
from django.utils.translation import ugettext_lazy as _

code = str(random.randrange(1000, 9999))
code = {"OTP": code}


class RegistrationViewSet(
    MultiSerializerViewSetMixin,
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet
):
    queryset = ApplicationUser.objects.all()
    serializer_class = RegistrationSerializer
    serializer_action_classes = {
        'check_user_data': CheckUserDataSerializer,
        'send_sms': CheckPhoneSerializer,
        'check_sms': CheckCodeSerializer,
    }
    permission_classes = [AllowAny]

    @action(methods=['post'], detail=False, permission_classes=(AllowAny,), url_path='check')
    def check_user_data(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if not self.request.data['password'] == self.request.data['confirm_password']:
            raise ValidationError(_('Your password is not match!!'))

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    @action(methods=['post'], detail=False, permission_classes=[AllowAny], url_path='send_sms')
    def send_sms(self,*args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response((serializer.data, code))

    @action(methods=['post'], detail=False, permission_classes=[AllowAny], url_path='check_sms')
    def check_sms(self,*args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if serializer.data != code:
            raise ValidationError('Not Verified Please enter correct!!')
        return Response("Verified Successfully!!")
