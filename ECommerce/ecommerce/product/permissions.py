from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from ecommerce.custom_auth.models import ApplicationUser


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.user.user_type)
        # if request.user.user_type == 'seller':
        #     return True
        # return False

        if request.user.is_authenticated:
            print(request.user.user_type)
            return request.user.user_type == ApplicationUser.USER_TYPES.seller
        else:
            raise PermissionDenied(_('Authentication required!!'))


class IsSellerCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == ApplicationUser.USER_TYPES.user
