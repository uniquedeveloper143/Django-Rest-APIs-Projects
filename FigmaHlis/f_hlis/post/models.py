from django.db import models
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from f_hlis.custom_auth.models import ApplicationUser
from f_hlis.post.utils import validate_comma_separated_integer_list, get_post_photo_path


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, null=True, blank=True,unique=True)


class Post(TimeStampedModel):
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=True, blank=True)
    description = models.TextField(max_length=556, null=True, blank=True)
    tags = models.CharField(max_length=100, null=True, blank=True, validators=[validate_comma_separated_integer_list])
    hash_tag = models.CharField(max_length=256, null=True, blank=True, validators=[validate_comma_separated_integer_list])
    file = models.FileField(null=True, blank=True, upload_to=get_post_photo_path)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)


class Like(TimeStampedModel):
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')

    def __str__(self):
        return f'{self.user}'


class Comment(TimeStampedModel):
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comments = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')

    def __str__(self):
        return f'{self.user}'
