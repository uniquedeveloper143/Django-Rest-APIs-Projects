from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from math import radians, cos, sin, asin, sqrt

from rest_framework.filters import SearchFilter

from vendor.category.models import City,Category,Product,Shop
from vendor.custom_auth.models import ApplicationUser
from vendor.custom_auth.serializers import BaseUserSerializer


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'city')


class CategorySerializer(serializers.ModelSerializer):
    city_details = CitySerializer(source='city', read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'city_details')


class ShopSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    vendor_details = BaseUserSerializer(source='vendor', read_only=True)
    miles = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ('vendor_details', 'category_details',  'id', 'vendor', 'name', 'category', 'ratings', 'address', 'image', 'miles')

    def get_ratings(self, obj):
        count = Shop.objects.all()
        cal = 0
        for c in count:
            cal += c.ratings
        return "{0:.2f}".format(cal/len(count))

    def get_miles(self, obj):
        # lat1 = 53.32055555555556
        # lat2 = 53.31861111111111
        # lon1 = -1.7297222222222221
        # lon2 = -1.6997222222222223

        data = ApplicationUser.objects.filter(shop=obj).first()
        user = self.context['request'].user
        print(user.longitude)
        lon1 = radians(data.longitude)
        lon2 = radians(user.longitude)
        lat1 = radians(data.latitude)
        lat2 = radians(user.latitude)

        # lon1 = radians(lon1)
        # lon2 = radians(lon2)
        # lat1 = radians(lat1)
        # lat2 = radians(lat2)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))
        # Radius 6371 of earth in kilometers. Use 3956 for miles
        r = 3956
        return (c * r)


class ProductSerializer(serializers.ModelSerializer):
    shop_details = ShopSerializer(source='shop', read_only=True)

    class Meta:
        model = Product
        fields = ('shop_details', 'id', 'name', 'price', 'description', 'slug', 'image')
