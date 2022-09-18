import re
from typing import Type

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework import permissions, status, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError ,NotFound
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from django_filters.rest_framework import DjangoFilterBackend
from unicef_restlib.pagination import DynamicPageNumberPagination
from templated_email import send_templated_mail

from ecommerce.custom_auth.models import PasswordResetId, Address
from ecommerce.custom_auth.permissions import IsSelf, IsAddressCreator
from ecommerce.custom_auth.serializers import AccessTokenSerializer, UserAuthSerializer, BaseUserSerializer, \
    UserPhotoSerializer, AttachmentSerializer, PasswordValidationSerializer, ChangePasswordSerializer, AddressSerializer
from ecommerce.utils.permissions import IsReadAction
from ecommerce.registrations.serializers import RegistrationSerializer
# from ecommerce.utils.serializers import add_serializer_mixin

User = get_user_model()


class UserAuthViewSet(viewsets.ViewSet):
    NEW_TOKEN_HEADER = 'X-Token'
    access_token_serializer_class = AccessTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_access_token_serializer(self, **kwargs):
        return self.access_token_serializer_class(data=self.request.data, **kwargs)

    @classmethod
    def get_success_headers(cls, user):
        return {cls.NEW_TOKEN_HEADER: user.user_auth_tokens.create().key}
    def _auth(self, request, *args, **kwargs):
        auth_serializer = UserAuthSerializer(data=request.data, context={'request': request, 'view': self})
        auth_serializer.is_valid(raise_exception=True)

        user = authenticate(request, **auth_serializer.data)
        if not user:
            raise ValidationError("Invalid credentials")

        user_details = BaseUserSerializer(
            instance=user, context={'request': request, 'view': self}).data
        user_details.update(self.get_success_headers(user)
        )
        return Response(data=user_details, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny],
            url_name='classic', url_path='classic')
    def classic_auth(self, request, *args, **kwargs):
        return self._auth(request, *args, **kwargs)     #for_agent=False,

    # @action(methods=['post'], detail=False, permission_classes=[AllowAny], url_path='classic', url_name='classic')
    # def classic_auth(self, request, *args, **kwargs):
    #     return self._auth(request, *args, **kwargs)

    @action(methods=['delete'], detail=False)
    def logout(self, request, *args, **kwargs):
        # todo: decide whhther we should remove all token or only the current one
        if request.user.user_auth_tokens.count() > 1:
            self.request.auth.delete()
        else:
            request.user.user_auth_tokens.all().delete()
        return Response("Logout Successfully", status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsReadAction | IsSelf]
    lookup_field = 'uuid'
    pagination_class = DynamicPageNumberPagination

    filter_backends = (DjangoFilterBackend, SearchFilter)

    search_fields = ['full_name', 'last_name', 'first_name']
    ordering = ['full_name']

    def get_permissions(self):
        if self.action in ['create', 'metadata']:
            return [AllowAny()]

        return super().get_permissions()

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        if self.kwargs[lookup_url_kwarg] == 'me':
            return self.request.user

        return super().get_object()

    def _get_base_serializer_class(self):
        if self.action in ['create', 'metadata']:
            return RegistrationSerializer

        if self.action == 'list':
            return BaseUserSerializer

        if self.action == 'set_photo':
            return UserPhotoSerializer

        if self.action == 'set_attachment':
            return AttachmentSerializer

        if self.action == 'password_reset_change_password':
            return PasswordValidationSerializer

        if self.action == 'change_password':
            return ChangePasswordSerializer

        if self.get_object() == self.request.user:
            return BaseUserSerializer

        return BaseUserSerializer

    def get_serializer_class(self) -> Type[BaseSerializer]:
        serializser_class = self._get_base_serializer_class()
        # if 'with_statistics' in self.request.query_params or self.action != 'list':
        #     serializser_class = add_serializer_mixin(serializser_class, UserStatisticSerializer)

        return serializser_class

    def get_queryset(self):
        queryset = super().get_queryset()

        if 'with_statistics' in self.request.query_params:
            queryset = queryset.with_statistic()

        return queryset

    @action(methods=['post'], detail=True, permission_classes=[permissions.AllowAny, IsSelf],
            url_path='photo/update_or_create', url_name='set_photo')
    def set_photo(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(request.user, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True, permission_classes=[permissions.AllowAny, IsSelf],
            url_path='photo/(?P<id>[0-9]+)', url_name='delete_photo')
    def delete_photo(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        user.photo.delete()
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny, IsSelf],
            url_path='reset-password-email', url_name='reset_password_email')
    def reset_password_email(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_email = request.data.get('email')
        if not user_email:
            raise ValidationError(_("Email fields is required."))

        user_model = User
        user = user_model.objects.filter(email__iexact=user_email).first()
        if not user:
            raise NotFound(_("User doesn't exists."))

        password_reset_obj = PasswordResetId.objects.create(user=user)
        site = get_current_site(request)
        print(password_reset_obj)

        # send_templated_mail(
        #     template_name="user_password_reset",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[user.email],
        #     context={
        #         'domain': site.domain,
        #         'password_reset_id': password_reset_obj.id,
        #         'protocol': 'https' if getattr(settings, 'FRONTEND_USE_HTTPS', False) else 'http',
        #         'full_name': user.full_name,
        #     }
        # )

        return Response(_("Email has been sent."))

    @action(methods=['post'], url_name='reset_change_password', url_path='reset-change-password/(?P<password_reset_id>.*)', detail=False,
            permission_classes=[permissions.AllowAny])
    def password_reset_change_password(self, request, *args, **kwargs):
        password_reset_obj = get_object_or_404(
            PasswordResetId,
            pk=self.kwargs.get('password_reset_id'),
            expiration_time__gt=timezone.now()
        )
        serializer = self.get_serializer_class()(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=password_reset_obj.user.id)
        user.set_password(serializer.data['password'])
        user.save()

        PasswordResetId.objects.filter(pk=password_reset_obj.pk).delete()
        return Response(_("Password reset Successfully!"))

    @action(methods=['post'], url_name='change_password', url_path='change-password', detail=False)
    def change_password(self, request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.set_password(serializer.data['new_password'])
        user.save()
        return Response(_("Password update Successfully"))


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction | IsAddressCreator]
    pagination_class = DynamicPageNumberPagination

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('user__uuid', )
    search_fields = ('name', )
    ordering = '-created'



