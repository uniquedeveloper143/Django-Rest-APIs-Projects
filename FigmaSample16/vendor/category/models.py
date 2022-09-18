from django.db import models
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

from vendor.custom_auth.models import ApplicationUser
from vendor.custom_auth.utils import get_category_photo_path, get_sub_category_photo_path, get_product_photo_path


class City(TimeStampedModel):
    city = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return f'{self.city}'


class Category(TimeStampedModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(
        upload_to=get_category_photo_path,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f'{self.name}'


class Shop(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vendor = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    ratings = models.FloatField(null=True, blank=True)
    image = models.ImageField(
        upload_to=get_sub_category_photo_path,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Shop')
        verbose_name_plural = _('Shops')

    def __str__(self):
        return f'{self.name}'


class Product(TimeStampedModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    slug = models.SlugField(_('slug'), max_length=250, null=True, blank=True)
    image = models.ImageField(
        upload_to=get_product_photo_path,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
