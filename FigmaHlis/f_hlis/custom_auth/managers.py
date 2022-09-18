from django.contrib.auth.models import UserManager
from django.db.models import QuerySet


class ApplicationUserManager(UserManager):
    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email):
        if not email:
            return None
        return super().normalize_email(email)

    def get_by_natural_key(self, value):
        return self.get(**{'%s__iexact' % self.model.USERNAME_FIELD: value})
