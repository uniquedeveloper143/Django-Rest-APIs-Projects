from django.urls import path,include
from rest_framework import routers
from ecommerce.product import views


router = routers.SimpleRouter()
router.register('', views.ProductViewSet, basename='product')
# router.register('product_photo', views.ProductPhotoViewSet, basename='product_photo')

app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
]
