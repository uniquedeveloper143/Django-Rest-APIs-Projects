from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ecommerce.product.models import Product, ProductPhoto
from ecommerce.product.permissions import IsSeller, IsSellerCreator, IsUser
from ecommerce.product.serializers import ProductSerializer, ProductPhotoSerializer
from ecommerce.utils.permissions import IsReadAction


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction | IsSeller, IsSellerCreator]
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name',)
    ordering = 'name'
    # filterset_fields = ('user__uuid',)


class ProductPhotoViewSet(viewsets.ModelViewSet):
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsReadAction | IsSeller & IsSellerCreator]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('image',)
    ordering = 'image'
    # filterset_fields = ('user__uuid',)

#
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated, IsReadAction | IsSeller, IsSellerCreator]
#
#     lookup_field = 'slug'
#
#     # def _get_base_serializer_class(self):
#     #     if self.action == 'add_image':
#     #         return ProductPhotoSerializer
#
#     @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated, IsReadAction | IsSeller, IsSellerCreator],
#             url_path='add_image', url_name='add_image', serializer_class='ProductPhotoSerializer')
#     def add_image(self, request, args, *kwargs):
#         product = self.get_object()  # login user
#
#         # self.check_object_permissions(request, user)
#         # data = request.data.update(request.data[user])
#         serializer = ProductPhotoSerializer(data=request.data)
#
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         data = serializer.validated_data
#         data.update({'product': product})
#
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @action(methods=['delete'], detail=True, permission_classes=[permissions.IsAuthenticated, IsSeller, IsProductCreator],
    #         url_path='delete_image/(?P<id>[0-9]+)', url_name='delete_image')
    # def delete_photo(self, request, args, *kwargs):
    #     get_object_or_404(ProductPhoto, pk=self.kwargs.get('id')).delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #

