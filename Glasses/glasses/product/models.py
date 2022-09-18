from django.contrib.auth import get_user_model
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
from django.db import models
from django.utils.translation import ugettext_lazy as _
from glasses.category.models import SubCategory
from glasses.utils.utils import get_product_photo_path

User = get_user_model()


class Product(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=100, null=True, blank=True)
    slug = models.SlugField(_('slug'), max_length=250, )
    description = models.TextField(_('description'), null=True, blank=True)
    price = models.FloatField(_('selling price'))
    sku_code = models.CharField(_("SKU Code"), max_length=100, null=True, blank=True)
    frame_size = models.CharField(_("Frame Size"), max_length=100, null=True, blank=True)
    frame_width = models.FloatField(_("Frame Width"))
    color = models.CharField(_('Color'), max_length=100, null=True, blank=True)
    stocks = models.IntegerField(_('number of stocks'), null=True, blank=True, default=0)
    rating = models.FloatField(_("Ratings"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_photo_details')
    image = models.ImageField(
        upload_to=get_product_photo_path,
        height_field='height',
        width_field='width',
        null=True,
        blank=True
    )
    width = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.product

    def save(self, *args, **kwargs):
        if self.image and (not self.width or not self.height):
            self.width = self.image.width
            self.height = self.image.height

        super().save(*args, **kwargs)


class Dummy(models.Model):
    title = models.CharField(_("Title"), max_length=100, null=True, blank=True)
    price = models.FloatField(_('price'), null=True, blank=True)
    date = models.DateField(_("Date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Dummy")
        verbose_name_plural = _("Dummy")

    def __str__(self):
        return f'{self.name}'
