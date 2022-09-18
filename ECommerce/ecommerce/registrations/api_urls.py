from django.urls import path,include
from  rest_framework.routers import SimpleRouter

from ecommerce.registrations.views import RegistrationViewSet

router = SimpleRouter()

router.register('', RegistrationViewSet, basename='registration')

app_name = 'registrations'
urlpatterns = [
    path('', include(router.urls)),
]