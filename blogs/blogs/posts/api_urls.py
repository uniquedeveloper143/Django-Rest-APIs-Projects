from django.urls import path, include
from rest_framework import routers
from unicef_restlib.routers import NestedComplexRouter

from blogs.posts import api

router = routers.SimpleRouter()
router.register('', api.PostViewSet, basename='posts')

post_router = NestedComplexRouter(router, r'')
post_router.register(r'photos', api.PostPhotosViewSet, basename='post-photos')


app_name = 'posts'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_router.urls)),
]
