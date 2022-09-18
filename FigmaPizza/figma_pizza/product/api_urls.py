from django.urls import path,include
from rest_framework import routers
from figma_pizza.product import views

router = routers.SimpleRouter()

# router.register('', views.UserAuthViewSet, basename='product')

app_name = 'product'

urlpatterns = [

        path('', include(router.urls)),
]

