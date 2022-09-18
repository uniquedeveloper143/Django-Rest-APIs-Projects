from django.urls import path, include
from rest_framework import routers
from glasses.registrations.views import RegistrationViewSet

router = routers.SimpleRouter()
router.register('', RegistrationViewSet, basename='registrations')

app_name = 'registrations'

urlpatterns = [

        path('', include(router.urls)),
]
