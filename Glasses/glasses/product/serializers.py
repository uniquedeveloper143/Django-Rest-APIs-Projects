from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from glasses.category.serializers import SubCategorySerializer
from glasses.product.models import ProductPhoto, Product, Dummy


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ('image', 'width', 'height')


class ProductSerializer(serializers.ModelSerializer):
    sub_category_details = SubCategorySerializer(source='sub_category', read_only=True)
    product_photo_details = ProductPhotoSerializer(required=False, many=True)

    class Meta:
        model = Product
        fields = ('user', 'product_photo_details', 'sub_category_details', 'sub_category', 'name', 'slug', 'price', 'description', 'sku_code', 'color', 'rating', 'stocks', 'frame_size', 'frame_width')
        read_only_fields = ('slug', )
        validators = [UniqueTogetherValidator(queryset=Product.objects.all(), fields=('name',))]


class DummySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dummy
        fields = ('id', 'title', 'price', 'date')
