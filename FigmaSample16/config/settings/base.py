import environ

env = environ.Env()
environ.Env.read_env()

root = environ.Path(__file__) - 3
# print('main root ', root)
apps_root = root.path('vendor')
# print('second main root ', apps_root)
# Build paths inside the project like this: os.path.join(BASE_DIR,....)
BASE_DIR = root()
# print('base dir', BASE_DIR)

SECRET_KEY = env('SECRET_KEY')

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

#UDRT INSTALLED APPS
THIRD_PARTY_APPS = [
    'rest_framework',
    'drf_secure_token',
    'django_filters',
]

#USER MODELS APPS
LOCAL_APPS = [
    'vendor.custom_auth',
    'vendor.registrations',
    'vendor.category',
    # 'ecommerce.product',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

AUTH_USER_MODEL = 'custom_auth.ApplicationUser'

AUTHENTICATION_BACKENDS = (
    'vendor.custom_auth.auth_backends.model_backends.CustomModelBackend',
)

# Django rest framework configuration

from rest_framework.permissions import IsAuthenticated

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'drf_secure_token.authentication.SecureTokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

}

PROJECT_FULL_NAME = env('PROJECT_FULL_NAME', default='FigmaSample16')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root('vendor', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = root('static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATICFILES_DIRS = [
    root('vendor', 'assets'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = root('media')


IMAGES_PATH_UER_PHOTOS = 'user_photos'
DOCUMENTS_PATH = 'documents'
PRODUCT_PHOTO_PATH = 'product_image'
CATEGORY_PHOTO_PATH = 'category_image'
SHOP_PHOTO_PATH = 'shop_image'



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
