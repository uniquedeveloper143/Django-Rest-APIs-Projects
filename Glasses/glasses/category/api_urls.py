from django.urls import path, include
from glasses.category import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register('category', views.CategoryViewSet, basename='category')
router.register('sub_category', views.SubCategoryViewSet, basename='sub_category')

app_name = 'category'

urlpatterns = [

        path('', include(router.urls)),
]
