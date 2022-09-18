import re,uuid

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils.regex_helper import _lazy_re_compile


def string_list_validator(sep=',', message=None, code='invalid', allow_negative=False):
    regexp = _lazy_re_compile(r'^%(neg)s\w+(?:%(sep)s%(neg)s\w+)*\Z' % {
        'neg': '(-)?' if allow_negative else '',
        'sep': re.escape(sep),
    })
    return RegexValidator(regexp, message=message, code=code)


validate_comma_separated_integer_list = string_list_validator(
    message=_('Enter only comma separated by commas.'),
)


def get_post_photo_path(instance, filename):
    return '{}/{}/{}'.format(settings.POST_PHOTO_PATH, uuid.uuid4(), filename)
