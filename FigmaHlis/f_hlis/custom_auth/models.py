import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from f_hlis.custom_auth.managers import ApplicationUserManager


class ApplicationUser(
    AbstractBaseUser,
    PermissionsMixin,
    # UserPhotoMixin,
):
    USER_TYPES = Choices(
        ('user', 'User'),
        ('seller', 'Seller'),
    )

    username_validator = UnicodeUsernameValidator()
    uuid = models.UUIDField(
        verbose_name=_('uuid'),
        unique=True,
        help_text=_('Required. A 32 hexadecimal digits number as specified in RFC 4122.'),
        error_messages={
            'unique': _('A user with that username is already exits.'),
                        },
        default=uuid.uuid4,
    )
    username = models.CharField(
        verbose_name=_('Username'),
        max_length=120,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Required. A 32 hexadecimal digits number as specified in RFC 4122'),
        error_messages={
            'unique': _('A user with that username already exists.')
        }
    )
    email = models.EmailField(_('email Address'), null=True, blank=True,unique=True,
                              error_messages={
                                  'unique': _("A user with that eamil already exits."),
                              },)
    is_email_verified = models.BooleanField('email verified', default=True)
    first_name = models.CharField(_('First Name'), max_length=100, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=100, blank=True)
    about = models.TextField(_("About me"), max_length=1000, blank=True)
    is_active = models.BooleanField(_('Staff status'), default=True, help_text=_(
        'Designates whether the user can log into this admin site.'
    ),)
    is_staff = models.BooleanField(_('Active'), default=False, help_text=_(
        'Designates whether this user should be treated as active.'
        'Unselected this instead of deleting accounts.'
    ),)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)
    last_user_activity = models.DateTimeField(_('last activity'), default=timezone.now)
    phone = PhoneNumberField(_('Phone'),null=True, unique=True, blank=True)
    user_type = models.CharField(max_length=40, choices=USER_TYPES, default=USER_TYPES.user)
    country = CountryField(blank=True,default='IN')

    soucial_id = models.CharField(max_length=256,null=True,blank=True)
    objects = ApplicationUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email or str(self.uuid)

    def update_last_activity(self):
        now = timezone.now()
        self.last_user_activity = now
        super.save(update_fields=('last_user_activity', 'last_modified'))