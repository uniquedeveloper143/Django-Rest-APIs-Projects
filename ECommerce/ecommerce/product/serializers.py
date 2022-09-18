from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator

from ecommerce.category.serializers import CategorySerializer
from ecommerce.product.models import Product,ProductPhoto


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        # fields = ('product', 'image', 'width', 'height',)
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    product_photo_details = ProductPhotoSerializer(required=False, many=True)

    class Meta:
        model = Product
        fields = ('user', 'category', 'name', 'slug', 'description', 'price', 'discount', 'stocks', 'category_details',
                  'product_photo_details')
        read_only_fields = ('slug', )

        validators = [UniqueTogetherValidator(queryset=Product.objects.all(), fields=('name',))]

    # def validate(self,attrs):

    # def create(self, request, *args, **kwargs):
    #     # Override create method to prevent duplicate object creation
    #     serializer = ProductSerializer(data=self.request.data)
    #     serializer.is_valid(raise_exception=True)
    #     # user = self.request.user
    #     product = serializer.validated_data['name']
    #     obj, created = Product.objects.get_or_create(product=product, deleted=False)
    #     if not created:
    #         serializer.save()
    #         return Response(status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(status=status.HTTP_409_CONFLICT)



