import uuid as uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from model_utils import Choices
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from blogs.custom_auth.managers import ApplicationUserManager
from blogs.custom_auth.mixins import UserPhotoMixin
from blogs.custom_auth.utils import set_password_reset_expiration_time


class ApplicationUser(
    AbstractBaseUser,
    UserPhotoMixin,
    PermissionsMixin
):
    GENDER_TYPES = Choices(
        ("male", "Male"),
        ("female", "Female"),
    )

    username_validator = UnicodeUsernameValidator()
    uuid = models.UUIDField(
        verbose_name=_('uuid'),
        unique=True,
        help_text=_('Required. A 32 hexadecimal digits number as specified in RFC 4122.'),
        error_messages={
            'unique': _('A user with that uuid already exists.'),
        },
        default=uuid.uuid4,
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    email = models.EmailField(_('email address'), null=True, blank=True, unique=True,
                              error_messages={'unique': _('A user with that email already exists.')}, )
    is_email_verified = models.BooleanField(_('email verified'), default=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    fullname = models.CharField(_('full name'), max_length=300, blank=True,
                                help_text=_('Full name as it was returned by social provider'))
    about = models.TextField(_('about me'), max_length=1000, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)
    last_user_activity = models.DateTimeField(_('last activity'), default=timezone.now)
    phone = PhoneNumberField(_('Phone'), null=True, blank=True, unique=True,
                             error_messages={'unique': _('A user with that phone already exists.')}, )
    gender = models.CharField(max_length=10, choices=GENDER_TYPES, default=GENDER_TYPES.male)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    city = models.CharField(_('city'), max_length=100, null=True, blank=True)

    objects = ApplicationUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username or self.fullname or self.email or self.first_name or str(self.uuid)

    def save(self, *args, **kwargs):
        if self.photo and (not self.width_photo or not self.height_photo):
            self.width_photo = self.photo.width
            self.height_photo = self.photo.height

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

        # full name assignment
        if not self.fullname.strip():
            if self.first_name and self.last_name:
                self.assign_full_name_to_the_object()

        if self.fullname:
            self.assign_first_last_name_to_the_object()

        return super(ApplicationUser, self).save(*args, **kwargs)

    def assign_full_name_to_the_object(self):
        self.fullname = f'{self.first_name} {self.last_name}'.strip()

    def assign_first_last_name_to_the_object(self):
        fullname = self.fullname.split(' ')
        self.first_name = fullname[0]
        if len(fullname) > 1:
            self.last_name = fullname[1]
        else:
            self.last_name = fullname[0]

    def update_last_activity(self):
        now = timezone.now()

        print(self.last_user_activity)
        self.last_user_activity = now
        self.save(update_fields=('last_user_activity', 'last_modified'))


class PasswordResetId(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiration_time = models.DateTimeField(default=set_password_reset_expiration_time)

    class Meta:
        verbose_name = 'Password reset id'
