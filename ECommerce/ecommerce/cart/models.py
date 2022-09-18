from django.db import models
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

from ecommerce.custom_auth.models import ApplicationUser
from ecommerce.product.models import Product


class Cart(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    # slug = models.SlugField(_('slug'), max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f'{self.product}'

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.product)
    #     super().save(*args, **kwargs)
