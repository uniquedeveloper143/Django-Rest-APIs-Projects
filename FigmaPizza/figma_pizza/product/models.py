from django.db import models
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from figma_pizza.custom_auth.models import ApplicationUser


class Product(TimeStampedModel):
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    name = models.CharField(_("Product Name"), max_length=100, null=True, blank=True, unique=True,
                            error_messages={
                                'unique': _('A product name that is already exists.')
                            })
    description = models.TextField(max_length=500, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True, null=True,blank=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        # upload_to=get_product_photo_path,
        height_field='height',
        width_field='width',
        null=True,
        blank=True
    )
    width = models.PositiveSmallIntegerField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image and (not self.width or not self.height):
            self.width = self.image.width_field
            self.height = self.image.height_field

        super().save(*args, **kwargs)


