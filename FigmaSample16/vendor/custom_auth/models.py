from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from model_utils import Choices
from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
from phonenumber_field.modelfields import PhoneNumberField

from vendor.custom_auth.managers import ApplicationUserManager
from vendor.custom_auth.utils import set_password_reset_expiration_time


class ApplicationUser(
    AbstractBaseUser,
    PermissionsMixin,
):
    USER_TYPES = Choices(
        ('user', 'User'),
        ('vendor', 'Vendor')
    )

    uuid = models.UUIDField(
        verbose_name=_('uuid'),
        unique=True,
        help_text=_('Required. A 32 hexadecimal digits '),
        error_messages={
            'unique': _('A user with that uuid already exits.'),
        },
        default=uuid.uuid4
    )

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name=_('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Required. A 32 hexadecimal digits number as specified in RFC 4122.'),
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )

    email = models.EmailField('Email Address', null=True, blank=True, unique=True,
                              error_messages={
                                  'unique': _("A user that email already exists."),
                              },)
    is_email_verified = models.BooleanField('Email Verified', default=True),
    name = models.CharField(_('Name'), max_length=100, blank=True, null=True)
    is_active = models.BooleanField(_('Staff Status'), default=True, blank=True,
                                    help_text=_(
                                        'Designates whether the user can log into this admin site.'
                                    ),)
    is_staff = models.BooleanField(_('active'), default=False, help_text=_(
        'Designates whether this user should be treated as active.'
        'Unselected this instead of deleting accounts'
    ),)
    last_modified = models.DateTimeField('last modified', default=timezone.now)
    last_user_activity = models.DateTimeField(_('last activity'), default=timezone.now)
    phone = PhoneNumberField(_('Phone'), null=True, blank=True, unique=True)
    # address = models.CharField(_('Address'), max_length=200, null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default=USER_TYPES.user)
    check_agree = models.BooleanField(_('Agree'), default=False,  help_text=_(
        'Please check term and conditions.'
    ), )
    longitude = models.DecimalField(decimal_places=10, null=True, blank=True, max_digits=20)
    latitude = models.DecimalField(decimal_places=10, null=True, blank=True, max_digits=20)

    objects = ApplicationUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email or self.name or str(self.uuid)

    def update_last_activity(self):
        now = timezone.now()

        self.last_user_activity = now
        self.save(update_fields=('last_user_activity', 'last_modified'))


class PasswordResetId(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiration_time = models.DateTimeField(default=set_password_reset_expiration_time)

    class Meta:
        verbose_name = 'Password reset id'
