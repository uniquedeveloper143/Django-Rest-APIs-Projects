from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser

from vendor.category.models import Category, City, Product, Shop
from vendor.category.serializers import CategorySerializer,CitySerializer,ProductSerializer,ShopSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('vendor', 'category')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
