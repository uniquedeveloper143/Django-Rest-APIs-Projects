from django.conf import settings
from django.utils import timezone
import uuid


def set_password_reset_expiration_time():
    return timezone.now() + timezone.timedelta(days=1)


def get_category_photo_path(instance, filename):
    return '{}/{}/{}'.format(settings.CATEGORY_PHOTO_PATH, uuid.uuid4(), filename)


def get_sub_category_photo_path(instance, filename):
    return '{}/{}/{}'.format(settings.SHOP_PHOTO_PATH, uuid.uuid4(), filename)


def get_product_photo_path(instance, filename):
    return '{}/{}/{}'.format(settings.PRODUCT_PHOTO_PATH, uuid.uuid4(), filename)

