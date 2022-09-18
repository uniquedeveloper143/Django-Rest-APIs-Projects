from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from ecommerce.cart.models import Cart
from ecommerce.product.serializers import ProductPhotoSerializer, ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    product_photo_details = ProductPhotoSerializer(required=False, many=True)

    class Meta:
        model = Cart
        fields = "__all__"
        # read_only_fields = ('slug',)

        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=('product',)
            )
        ]


    # cart = Cart.objects.filter(user=self.context['request'].user)
    # print(cart)

    # def validate(self, attrs):
    #     validate_data = super().validate(attrs)
    #     try:
    #         data = Cart.objects.filter(user=self.context['request'].user, product=validate_data['product'])
    #         if data:
    #             raise ValidationError('Product has already exists!!')
    #     except Cart.DoesNotExist:
    #         validate_data.update({'user': self.context['request'].user})
    #
    #     return validate_data



