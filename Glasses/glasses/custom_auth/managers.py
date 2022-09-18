from django.contrib.auth.models import UserManager
from django.db.models import QuerySet


class ApplicationUserQuerySet(QuerySet):
    def with_statistic(self):
        return self.with_filters_amount()

    def with_filters_amount(self):
        return self.annotate(
            filters_amount=1,
        )


class ApplicationUserManager(UserManager.from_queryset(ApplicationUserQuerySet)):
    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email):
        if not email:
            # using None instead of empty string in there's no email to bypass unique=True constraints
            return None
        return super().normalize_email(email)
