from django.conf import settings
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from ecommerce.cart.models import Cart
from ecommerce.custom_auth.models import Address
from ecommerce.product.models import Product


class Order(TimeStampedModel):
    PAYMENT_TYPE = Choices(
        ("cod", "Cash On Delivery"),
        ("upi", "UPI"),
        ("card", "Card"),
    )

    ORDER_STATUS = Choices(
        ("pending", "Pending"),
        ("canceled", "Canceled"),
        ("returned", "Returned"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("on_the_way", "On The Way"),
        ("dispatch", "Dispatch"),
        ("shipped", "Sipped"),
        ("delivered", "Delivered"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    shipping_charge = models.FloatField(_('Shipping Charge'), default=0, null=True)
    total_product = models.IntegerField(_('Total Product'), default=0, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE, default=PAYMENT_TYPE.cod)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS, default=ORDER_STATUS.pending)
    total_amount = models.FloatField(_('Total Amount'), default=0, null=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{self.user}'


class OrderDetails(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    price = models.FloatField(_('selling price'))
    quantity = models.FloatField(_('Quantity'))
    sub_total = models.FloatField(_('Sub Total'), default=0, null=True)

    class Meta:
        verbose_name = _('OrderDetail')
        verbose_name_plural = _('OrderDetails')

    def __str__(self):
        return f'{self.order}'
