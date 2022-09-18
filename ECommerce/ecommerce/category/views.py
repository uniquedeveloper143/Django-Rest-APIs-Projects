from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
# Create your views here.
from rest_framework.filters import SearchFilter, OrderingFilter
from unicef_restlib.pagination import DynamicPageNumberPagination

from ecommerce.category.models import Category
from ecommerce.category.serializers import CategorySerializer
from ecommerce.custom_auth.permissions import IsSelf
from ecommerce.utils.permissions import IsReadAction


class CategoryViewSet(viewsets.ModelViewSet):

    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     queryset = super().get_queryset()
    #     # queryset = Category.objects.all()

    #     search = self.request.query_params.get('search')
    #     if search is not None:
    #         return Category.objects.filter(name__iexact=search)
    #     return super().get_queryset()

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsReadAction]
    # pagination_class = DynamicPageNumberPagination
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filterset_fields = ('user__uuid',)

    # search_fields = ('=slug', '=name')
    search_fields = ('name', )
    ordering = '-id'
    # username_query_dict = {'username__iexact': username}
