from django.urls import path, include
from glasses.custom_auth import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register('auth', views.UserAuthViewSet, basename='auth')

app_name = 'custom_auth'

urlpatterns = [

        path('', include(router.urls)),
]
