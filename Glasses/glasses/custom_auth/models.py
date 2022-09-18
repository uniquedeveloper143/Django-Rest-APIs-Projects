from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from model_utils import Choices
import uuid

from phonenumber_field.modelfields import PhoneNumberField

from glasses.custom_auth.managers import ApplicationUserManager


class ApplicationUser(
    AbstractBaseUser,
    # UserPhotoMixin,
    PermissionsMixin,
):

    USER_TYPES = Choices(
        ("user", "User"),
        ("seller", "Seller"),
    )

    GENDER_TYPES = Choices(
        ("male", "Male"),
        ("female", "Female"),
    )

    username = models.CharField(
        verbose_name=_('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Required. A 32 hexadecimal digits number as specified in RFT.'),
        error_messages={
            'unique': _('A user with that username already exists.')
        },
    )

    user_validator = UnicodeUsernameValidator()
    uuid = models.UUIDField(
        verbose_name=_('uuid'),
        unique=True,
        help_text=_('Required. A 32 hexadecimal digits number as specified in RFC 4122.'),
        error_messages={
            'unique':_('A user with that uuid already exits. ')
        },
        default=uuid.uuid4,
    )
    email = models.EmailField(_('email address'), null=True, blank=True, unique=True,
                              error_messages={
                                  'unique': _('A user that email already exists.')
                              },
                              )
    is_email_verified = models.BooleanField('email verified', default=True)
    first_name = models.CharField(_('First Name'), max_length=150, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=150, blank=True)
    full_name = models.CharField(_('Full Name'), max_length=150, blank=True,
                                 help_text=_("Full name as it was returned by social provider"))
    about = models.TextField(_('about me'), max_length=1000, blank=True)
    is_active = models.BooleanField(_('staff status'), default=True, help_text=_(
        'Designates whether the user can log into this admin site.'
    ),)
    is_staff = models.BooleanField(_('active'), default=False, help_text=_(
        'Designates whether this user should be treated as active.'
        'Unselect this instead of deleting accounts.'
    ),)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)
    last_user_activity = models.DateTimeField(_('last activity'), default=timezone.now)
    phone = PhoneNumberField(_('phone'), null=True, unique=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPES, default=GENDER_TYPES.male)
    date_of_birth = models.DateField(_('data of birth'), null=True, blank=True)
    city = models.CharField(_('city'), max_length=100, null=True, blank=True)
    is_deliver_orders = models.BooleanField(_('Do you want to orders?'), default=False)
    delivery_region = models.CharField(_('delivery region'), max_length=255, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default=USER_TYPES.user)

    objects = ApplicationUserManager()

    EMAIL_FIELDS = 'email'
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username or self.full_name, self.email or self.first_name or str(self.uuid)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)

        if not self.username:
            new_username = self.email.split('@')[0] if self.email else ''

            if self._meta.model._default_manager.filter(username=new_username).exists() or new_username == '':
                postfix = timezone.now().strftime('%Y%m%d%H%M%S')

                while self._meta.model._default_manager.filter(username=new_username + postfix).exists():
                    postfix = timezone.now().strftime('%Y%m%d%H%M%S')

                new_username += postfix
            self.username = new_username

        if not self.full_name.strip():
            if self.first_name and self.last_name:
                self.assign_full_name_to_the_object()
        if self.full_name:
            self.assign_first_last_name_to_the_object()

        return super(ApplicationUser, self).save(*args, **kwargs)

    def assign_full_name_to_the_object(self):
        self.full_name = f'{self.first_name} {self.last_name}'.strip()

    def assign_first_last_name_to_the_object(self):
        fullname = self.full_name.split(' ')
        self.first_name = fullname[0]
        if len(fullname) > 1:
            self.last_name = fullname[1]
        else:
            self.first_name = fullname[0]

    def update_last_activity(self):
        now = timezone.now()

        self.last_user_activity = now
        self.save(update_fields=('last_user_activity', 'last_modified'))


