from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from unicef_restlib.views import MultiSerializerViewSetMixin

from blogs.custom_auth.models import ApplicationUser
from blogs.registrations.serializers import CheckPhoneSerializer, CheckUserDataSerializer, RegistrationSerializer
from blogs.utils.permissions import IsAPIKEYAuthenticated


class RegistrationViewSet(
    MultiSerializerViewSetMixin,
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = ApplicationUser.objects.all()
    serializer_class = RegistrationSerializer
    serializer_action_classes = {
        'check_user_data': CheckUserDataSerializer,
        'send_sms': CheckPhoneSerializer,
    }
    permission_classes = (AllowAny, IsAPIKEYAuthenticated,)

    @action(methods=['post'], permission_classes=(AllowAny, IsAPIKEYAuthenticated,), url_name='check',
            url_path='check', detail=False)
    def check_user_data(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        serializer.is_valid(raise_exception=True)

        # Send SMS code

        return Response(serializer.data)

    @action(permission_classes=(AllowAny, IsAPIKEYAuthenticated,), methods=['post'], url_name='send_sms_code',
            url_path='send-sms-code', detail=False)
    def send_sms(self, *args, **kwargs):
        """
        For manual sms code sending
        """
        serializer = self.get_serializer(data=self.request.data)

        serializer.is_valid(raise_exception=True)

        # Send SMS code

        return Response()
