from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from ecommerce.cart.models import Cart
from ecommerce.custom_auth.models import Address
from ecommerce.custom_auth.serializers import UserAuthSerializer, AddressSerializer, BaseUserSerializer
from ecommerce.order_place.models import Order, OrderDetails
from ecommerce.product.models import Product
from ecommerce.product.serializers import ProductSerializer


class OrderDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderDetails
        fields = ('product',)
        # fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    # address = AddressSerializer(required=False)
    address_details = AddressSerializer(source='address', read_only=True)
    order_details = OrderDetailsSerializer(many=True, read_only=True)

    # user_details = UserAuthSerializer(required=False, many=True)

    class Meta:
        model = Order
        fields = ('user', 'address', 'address_details', 'shipping_charge', 'payment_type', 'order_status', 'total_product', 'total_amount', 'order_details')
        # fields = '__all__'

    def create(self, validated_data):
        # ad = Address.objects.filter(user=self.context['request'].user, id=validated_data['address'].id).first()
        # print('--------->>>',ad.name)
        cart = Cart.objects.filter(user=self.context['request'].user)
        shipping_charge = self.validated_data['shipping_charge']
        address = self.validated_data['address']
        total = 0
        c = 0
        # print('Total -----', len(Order.objects.filter(user=self.context['request'].user)))
        if len(cart) == 0:
            raise ValidationError("Your cart is empty please add to cart!!")

        for i in cart:
            prod = Product.objects.filter(id=i.product.id).first()
            total += i.quantity * prod.price
            print(i.product.price)
            if c == 0:
                order = Order(user=i.user, total_product=len(cart), shipping_charge=shipping_charge, address=address,
                              total_amount=total)
                order.save()
                c = 1

            # order_id = Order.objects.filter(user=i.user).last()

            sub_total = i.quantity*prod.price
            order_details = OrderDetails(order=order, product=i.product, price=prod.price, quantity=i.quantity, sub_total=sub_total)

            # order_details = OrderDetails.objects.bulk_create([OrderDetails(order=order, product=i.product, price=prod.price, quantity=i.quantity, sub_total=sub_total)])

            order_details.save()

            i.delete()
        return order



