from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_dev_glasses',
        'USER':'root',
        'PASSWORD':'',
        'HOST':'127.0.0.1',
        'PORT':'3307'
    }
}

# E-mail settings

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = SERVER_EMAIL = env('SERVER_EMAIL_SIGNATURE') + '<%s>' % env('SERVER_EMAIL')
