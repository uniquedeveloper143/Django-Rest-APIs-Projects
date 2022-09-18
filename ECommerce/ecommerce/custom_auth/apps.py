from django.apps import AppConfig


class CustomAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # name = 'custom_auth'
    # name = 'ecommerce.custom_auth'       # this is the first way but suitable
    name = __name__.rpartition('.')[0]
