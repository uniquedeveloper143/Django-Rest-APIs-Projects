from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from glasses.category.models import Category, SubCategory
from glasses.category.serializers import CategorySerializer, SubCategorySerializer
from glasses.utils.permissions import IsReadAction


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction]

    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    search_fields = ('name',)

    @action(methods=['post'],permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser],url_path='add_cat', detail=False)
    def add_sub(self,*args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction]
    lookup_field = 'slug'
    # print("--->",queryset)

    @action(methods=['post'],permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser],url_path='add_sub',detail=False)
    def add_sub(self,*args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)


