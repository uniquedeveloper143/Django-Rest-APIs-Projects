from django.urls import path,include
from rest_framework import routers
from ecommerce.cart import views


router = routers.SimpleRouter()
router.register('', views.CartViewSet, basename='cart')

app_name = 'cart'

urlpatterns = [
    path('', include(router.urls)),
]
