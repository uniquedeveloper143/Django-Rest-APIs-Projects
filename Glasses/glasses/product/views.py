from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from glasses.product.models import Product, ProductPhoto, Dummy
from glasses.product.serializers import ProductSerializer, ProductPhotoSerializer, DummySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated, IsAdminUser],
            url_path='add_photo', url_name='add_photo')
    def add_photo(self, request, *args, **kwargs):
        product = self.get_object()
        # self.check_object_permissions(request, user)
        serializer = ProductPhotoSerializer(data=self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        data.update({"product": product})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @action(methods=['post'], permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser],
    #         url_path='add_photo', detail=False)
    # def add_photo(self, *args, **kwargs):
    #     serializer = self.get_serializer(data=self.request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_201_CREATED)
    #     serializer.save()
    #     return Response(serializer.data)

# class ProductPhotoViewSet(viewsets.ModelViewSet):
#     queryset = ProductPhoto.objects.all()
#     serializer_class = ProductPhotoSerializer
#     permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class DummyViewSet(viewsets.ModelViewSet):
    queryset = Dummy.objects.all()
    serializer_class = DummySerializer
    permission_classes = [permissions.AllowAny]
