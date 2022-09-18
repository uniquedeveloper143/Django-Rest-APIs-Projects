from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_prod_figma_hlis',
        'USER':'root',
        'PASSWORD':'',
        'HOST':'127.0.0.1',
        'PORT':'3307'
    }
}