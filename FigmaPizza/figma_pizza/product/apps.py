from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # name = 'product'
    name = __name__.rpartition('.')[0]
