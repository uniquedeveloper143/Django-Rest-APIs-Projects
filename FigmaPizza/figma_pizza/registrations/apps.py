from django.apps import AppConfig


class RegistrationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # name = 'registrations'
    name = __name__.rpartition('.')[0]

