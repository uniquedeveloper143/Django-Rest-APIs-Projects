from django.urls import path, include
from rest_framework import routers
from blogs.category import api

router = routers.SimpleRouter()
router.register('', api.CategoryViewSet, basename='category')

app_name = 'category'

urlpatterns = [
    path('', include(router.urls)),
]
