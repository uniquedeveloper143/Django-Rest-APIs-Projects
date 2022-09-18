from django.contrib.auth.models import UserManager


class ApplicationUserManager(UserManager):
    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email):
        if not email:
            # using None instead of empty string in there's no email to bypass unique=True constraints
            return None
        return super().normalize_email(email)
