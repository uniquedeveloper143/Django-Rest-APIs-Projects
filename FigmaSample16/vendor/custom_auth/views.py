from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from vendor.custom_auth.models import PasswordResetId
from vendor.custom_auth.serializers import AccessTokenSerializer, UserAuthSerializer, BaseUserSerializer
from django.utils.translation import ugettext as _

from vendor.registrations.serializers import ResetPasswordSerializer

User = get_user_model()


class UserAuthViewSet(viewsets.ViewSet):
    NEW_TOKEN_HEADER = 'MY-TOKEN'
    access_token_serializer_class = AccessTokenSerializer
    permission_classes = (permissions.AllowAny,)

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
            raise ValidationError("Invalid User!")

        user_details = BaseUserSerializer(
            instance=user, context={'request': request, 'view': self}).data
        user_details.update(self.get_success_headers(user))

        return Response(data=user_details, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, permission_classes=[AllowAny], url_path='login')
    def login(self, request, *args, **kwargs):
        return self._auth(request, *args, **kwargs)

    @action(methods=['delete'], detail=False)
    def logout(self, request, *args, **kwargs):
        if request.user.user_auth_tokens.count() > 1:
            self.request.auth.delete()
        else:
            request.user.user_auth_tokens.all().delete()
        return Response("logout Successfully!!")

    @action(methods=['post'], detail=False, permission_classes=[permissions.IsAuthenticated], url_path='reset_password')
    def reset_password(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            raise ValidationError(_('Username is required!!'))

        user_model = User
        email = user_model.objects.filter(email__iexact=username).first()
        phone = user_model.objects.filter(phone__iexact=username).first()
        if not email and not phone:
            raise NotFound(_('User does not exists.'))
        if email:
            password_id = PasswordResetId.objects.create(user=email)
        if phone:
            password_id = PasswordResetId.objects.create(user=phone)

        site = get_current_site(request)
        data = {"ReseteID": password_id.id}
        return Response(data)

    @action(methods=['post'], url_path='change_reset_password/(?P<password_reset_id>.*)',detail=False,permission_classes=[permissions.AllowAny])
    def change_reset_password(self, request, *args, **kwargs):
        password_id = get_object_or_404(PasswordResetId,
                                        pk=self.kwargs.get('password_reset_id'),
                                        expiration_time__gt=timezone.now()
                                        )

        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=password_id.user.id)
        user.set_password(serializer.data['password'])
        user.save()

        PasswordResetId.objects.filter(pk=password_id.pk).delete()
        return Response(_("Password reset successfully!!"))
