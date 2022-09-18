from _testcapi import raise_exception

from rest_framework.permissions import IsAdminUser
from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from f_hlis.custom_auth.serializers import AccessTokenSerializer, UserAuthSerializer, BaseUserSerializer

User = get_user_model()


class UserAuthViewSet(viewsets.ViewSet):
    NEW_TOKEN_HEADER = 'MY-TOKEN'
    access_token_serializer_class = AccessTokenSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_access_token_serializer(self, **kwargs):
        return self.access_token_serializer_class(data=self.request.data, **kwargs)

    @classmethod
    def get_success_headers(cls, user):
        return {cls.NEW_TOKEN_HEADER: user.user_auth_tokens.create().key}

    def _auth(self, request, *args, **kwargs):
        auth_serializer = UserAuthSerializer(data=self.request.data, context={'request': request,'view': self})
        auth_serializer.is_valid(raise_exception=True)

        user = authenticate(request, **auth_serializer.data)
        print('user  --',user)
        if not user:
            raise ValidationError("Invalid User")

        user_details = BaseUserSerializer(
            instance=user, context={'request': request, 'view': self}).data
        user_details.update(self.get_success_headers(user)
        )
        return Response(data=user_details, status=HTTP_201_CREATED)

    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny], url_path='classic')
    def classic_auth(self, request, *args, **kwargs):
        return self._auth(request, *args, **kwargs)

    @action(methods=['delete'], detail=False)
    def logout(self,request, *args, **kwargs):
        if request.user.user_auth_tokens.count() > 1:
            self.request.auth.delete()
        else:
            request.user.user_auth_tokens.all().delete()
        return Response("Logout Successfully!!", status=HTTP_200_OK)

