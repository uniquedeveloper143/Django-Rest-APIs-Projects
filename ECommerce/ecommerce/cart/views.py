from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from ecommerce.cart.models import Cart
from ecommerce.cart.permissions import IsCartCreator,IsSelf
from ecommerce.cart.serializers import CartSerializer
from ecommerce.custom_auth.models import ApplicationUser
from ecommerce.utils.permissions import IsReadAction
from django.db import models
from django.db.models import Prefetch, Sum, F


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated, IsCartCreator]
    # lookup_field = 'slug'
    # filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # search_fields = ('name',)
    # ordering = 'name'

    def get_queryset(self):
        # queryset = super().get_queryset()
        # print("---------", Cart.objects.filter(id=self.request.user.id))
        # print("--------->>", self.request.user.id)

        queryset = Cart.objects.filter(user=self.request.user.id)

        # u = ApplicationUser.objects.filter(id=Cart.user)
        # if u:
        #     # queryset = queryset.with_statistic()
        #     print("--------->>>>>>>>>", self.request.user)
        return queryset

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data.update(self.filter_queryset(self.get_queryset())
                             .aggregate(total=Sum(F('quantity')*F('product__price'), output_field=models.FloatField())))
        return response
