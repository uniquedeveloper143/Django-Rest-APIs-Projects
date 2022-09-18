from django.contrib.auth.models import UserManager
from django.db.models import QuerySet, Count, OuterRef, Subquery

from blogs.posts.models import Post
from blogs.utils.utils import SQCount


class ApplicationUserQuerySet(QuerySet):
    def with_statistic(self):
        return self.with_filters_amount()

    def with_filters_amount(self):
        # return self.annotate(
        #     filters_amount=Count(1),
        # )
        return self.annotate(
            filters_amount=SQCount(Post.objects.filter(author_id=OuterRef('id'))),
        )
        # return self.annotate(
        #     appointments_amount=SQCount(Post.objects.filter(author_id=OuterRef('id')))
        # )


class ApplicationUserManager(UserManager.from_queryset(ApplicationUserQuerySet)):
    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email):
        if not email:
            # using None instead of empty string if there's no email to bypass unique=True constraint
            return None
        return super().normalize_email(email)

    def get_by_natural_key(self, value):
        return self.get(**{'%s__iexact' % self.model.USERNAME_FIELD: value})
