from django.urls import path,include
from rest_framework import routers
from f_hlis.post import views
router = routers.SimpleRouter()

router.register('post', views.PostViewSet, basename='post')
router.register('like', views.LikeViewSet, basename='like')
router.register('comment', views.CommentViewSet, basename='comment')

app_name = 'post'

urlpatterns = [

        path('', include(router.urls)),
]

