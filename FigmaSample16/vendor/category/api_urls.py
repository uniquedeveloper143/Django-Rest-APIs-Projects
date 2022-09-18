from django.urls import path,include
from rest_framework import routers
from vendor.category import views

router = routers.SimpleRouter()

router.register('category', views.CategoryViewSet, basename='category')
router.register('city', views.CityViewSet, basename='city')
router.register('shop', views.ShopViewSet, basename='shop')
router.register('product', views.ProductViewSet, basename='product')

app_name = 'category'

urlpatterns = [

        path('', include(router.urls)),
]

