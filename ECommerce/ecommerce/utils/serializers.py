from copy import copy
from typing import Type, Any

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class ReadCreateOnlySerializerMixin(object):
    create_not_allowed_message = _('This serializer is not suitable to create instances.')

    @classmethod
    def create(cls, validated_data):
        raise NotImplementedError(cls.create_not_allowed_message)


class ReadUpdateOnlySerializerMixin(object):
    update_not_allowed_message = _('This serializer is not suitable to update instances.')

    @classmethod
    def update(cls, instance, validated_data):
        raise NotImplementedError(cls.update_not_allowed_message)


class ReadOnlySerializerMixin(ReadUpdateOnlySerializerMixin, ReadCreateOnlySerializerMixin):
    pass
