from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from blogs.category.models import Category
from blogs.utils.utils import get_post_photo_path


class Post(TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posts')
    title = models.CharField(_("Title"), max_length=200, help_text="The post title.")
    meta_title = models.TextField(_('Meta title'), null=True, blank=True,
                                  help_text="The meta title to be used for browser title and SEO.")
    slug = models.SlugField(_('Slug'), max_length=250, null=True, blank=True)
    published = models.BooleanField(_("Published?"), default=False)
    content = models.TextField(_("Post content"))

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PostPhoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_photos')
    image = models.ImageField(
        upload_to=get_post_photo_path,
        height_field='height',
        width_field='width',
        null=True,
        blank=True
    )
    width = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.image and (not self.width or not self.height):
            self.width = self.image.width
            self.height = self.image.height

        super().save(*args, **kwargs)
