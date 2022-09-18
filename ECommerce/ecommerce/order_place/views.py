from django.db.models import Sum, Count
from rest_framework import viewsets
from django.db import models
from ecommerce.cart.models import Cart
from ecommerce.order_place.models import Order
from ecommerce.order_place.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAuthenticated, IsCartCreator]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)

        return queryset

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        # response.data.update(self.filter_queryset(self.get_queryset()).aggregate(total=Count(('user'), output_field=models.FloatField())))
        response.data.update({"Total Orders ": len(Order.objects.filter(user=self.request.user))})

        return response
