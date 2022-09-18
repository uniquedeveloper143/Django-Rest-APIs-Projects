from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

#AMINS
# ADMINS = env.jon('ADMINS')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_prod_figma_pizza',
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