from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from glasses.custom_auth.models import ApplicationUser
from glasses.utils.utils import get_user_photo_random_filename, get_product_photo_path, get_category_product_photo_path


class Category(TimeStampedModel):
    # user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(_('Category name '), max_length=50, unique=True,
                                     error_messages={
                                         'unique': _('A category with that name is already exists!!')
                                     })
    slug = models.SlugField(_('Slug'), max_length=120, null=True, blank=True)

    class Meta:
        verbose_name = _("Category")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubCategory(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(_('Subcategory name '), max_length=50, unique=True,
                                     error_messages={
                                         'unique': _('A sub category with that name is already exists!!')
                                     })
    slug = models.SlugField(_('Slug'), max_length=125, null=True, blank=True)
    image = models.ImageField(
        upload_to=get_category_product_photo_path,
        height_field='height',
        width_field='width',
        null=True,
        blank=True
    )
    width = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _("Sub Category")

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        if self.image and (not self.width or not self.height):
            self.width = self.image.width
            self.height = self.image.height

        super().save(*args, **kwargs)

