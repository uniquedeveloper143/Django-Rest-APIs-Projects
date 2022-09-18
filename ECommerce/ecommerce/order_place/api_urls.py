from django.urls import path,include
from rest_framework import routers
from ecommerce.order_place import views


router = routers.SimpleRouter()
router.register('', views.OrderViewSet, basename='order')
# router.register('product_photo', views.ProductPhotoViewSet, basename='product_photo')

app_name = 'order_place'

urlpatterns = [
    path('', include(router.urls)),
]
