from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from blogs.category.models import Category
from blogs.category.serializers import CategorySerializer
from blogs.utils.permissions import IsAPIKEYAuthenticated, IsReadAction


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAPIKEYAuthenticated, IsReadAction]
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('title',)
    ordering_fields = ('title',)
    ordering = ('-created',)
