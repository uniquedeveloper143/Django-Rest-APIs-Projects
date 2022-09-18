from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_dev_figma_hlis',
        'USER':'root',
        'PASSWORD':'',
        'HOST':'127.0.0.1',
        'PORT':'3307'
    }
}