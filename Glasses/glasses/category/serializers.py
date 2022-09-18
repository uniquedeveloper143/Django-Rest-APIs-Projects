from rest_framework import serializers

from glasses.category.models import Category, SubCategory


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')
        read_only_fields = ('slug', )


class SubCategorySerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    name = serializers.CharField(required=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug', 'image', 'category_details')
        read_only_fields = ('slug',)
