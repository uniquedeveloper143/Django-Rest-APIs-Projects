from typing import Type

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from templated_email import send_templated_mail

from blogs.custom_auth.models import PasswordResetId
from blogs.custom_auth.permissions import IsSelf
from blogs.custom_auth.serializers import UserAuthSerializer, BaseUserSerializer, UserStatisticSerializerMixin, \
    UserPhotoSerializer, PasswordValidationSerializer, ChangePasswordSerializer
from blogs.utils.permissions import IsAPIKEYAuthenticated, IsReadAction
from blogs.utils.serializers import add_serializer_mixin

User = get_user_model()


class UserAuthViewSet(viewsets.ViewSet):
    NEW_TOKEN_HEADER = 'X-Token'
    permission_classes = (permissions.IsAuthenticated,)

    @classmethod
    def get_success_headers(cls, user):
        return {cls.NEW_TOKEN_HEADER: user.user_auth_tokens.create().key}

    def _auth(self, request, *args, **kwargs):
        auth_serializer = UserAuthSerializer(data=request.data, context={'request': request, 'view': self})
        auth_serializer.is_valid(raise_exception=True)

        user = authenticate(request, **auth_serializer.data)
        if not user:
            raise ValidationError('Invalid credentials')

        user_details = BaseUserSerializer(
            instance=user, context={'request': request, 'view': self}
        ).data
        user_details.update(self.get_success_headers(user))

        return Response(data=user_details, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny, IsAPIKEYAuthenticated],
            url_name='classic', url_path='classic')
    def classic_auth(self, request, *args, **kwargs):
        return self._auth(request, *args, for_agent=False, **kwargs)

    @action(methods=['delete'], detail=False, permission_classes=[permissions.AllowAny, IsAPIKEYAuthenticated])
    def logout(self, request, *args, **kwargs):
        request.user.user_auth_tokens.all().delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAPIKEYAuthenticated, IsReadAction | IsSelf]
    lookup_field = 'uuid'
    filter_backends = (DjangoFilterBackend, SearchFilter)

    search_fields = ['fullname']
    ordering = ['fullname']

    def get_permissions(self):
        if self.action in ['create', 'metadata']:
            return [AllowAny(), IsAPIKEYAuthenticated]

        return super().get_permissions()

    def _get_base_serializer_class(self):
        if self.action == 'list':
            return BaseUserSerializer

        if self.action == 'set_photo':
            return UserPhotoSerializer

        if self.action == 'password_reset_change_password':
            return PasswordValidationSerializer

        if self.action == 'change_password':
            return ChangePasswordSerializer

        return BaseUserSerializer

    @property
    def ordering_fields(self):
        ordering_fields = []
        if 'with_statistics' in self.request.query_params or self.action != 'list':
            ordering_fields += [
                'filters_amount'
            ]
        return ordering_fields

    def get_serializer_class(self) -> Type[BaseSerializer]:
        serializer_class = self._get_base_serializer_class()
        if 'with_statistics' in self.request.query_params or self.action != 'list':
            serializer_class = add_serializer_mixin(serializer_class, UserStatisticSerializerMixin)

        return serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()

        if 'with_statistics' in self.request.query_params:
            queryset = queryset.with_statistic()

        return queryset

    @action(methods=['post'], detail=True, permission_classes=[permissions.AllowAny, IsAPIKEYAuthenticated, IsSelf],
            url_path='photos/update_or_create', url_name='set_photo')
    def set_photo(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(request.user, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True, permission_classes=[permissions.AllowAny, IsAPIKEYAuthenticated, IsSelf],
            url_path='photos/(?P<id>[0-9]+)', url_name='delete_photo')
    def delete_photo(self, request, *args, **kwargs):
        user = self.get_object()
        self.check_object_permissions(request, user)
        user.photo.delete()
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny, IsAPIKEYAuthenticated],
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
            raise ValidationError(_("Email field is required."))

        user_model = User
        user = user_model.objects.filter(email__iexact=user_email).first()
        if not user:
            raise NotFound(_("User doesn't exists."))

        password_reset_obj = PasswordResetId.objects.create(user=user)
        site = get_current_site(request)

        send_templated_mail(
            template_name="user_password_reset",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            context={
                'domain': site.domain,
                'password_reset_id': password_reset_obj.id,
                'protocol': 'http',
                'fullname': user.fullname,
            }
        )

        return Response(_("Email has been sent."))

    @action(methods=['post'], detail=False, url_path='change-password', url_name='change_password')
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.data['new_password'])
        user.save()

        return Response(_("Password update successfully!"))
