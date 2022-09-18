from django.urls import path, include
from glasses.product import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register('product', views.ProductViewSet, basename='product')
router.register('dummy_data', views.DummyViewSet, basename='dummy_data')

app_name = 'product'

urlpatterns = [

        path('', include(router.urls)),
]
