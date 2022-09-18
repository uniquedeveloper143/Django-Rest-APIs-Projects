from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response

from blogs.posts.helpers import modify_input_for_multiple_files
from blogs.posts.models import Post, PostPhoto
from blogs.posts.permissions import IsSelf
from blogs.posts.serializers import PostSerializer, PostPhotoSerializer
from blogs.utils.permissions import IsAPIKEYAuthenticated, IsReadAction


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(published=True)
    permission_classes = [permissions.IsAuthenticated, IsAPIKEYAuthenticated, IsReadAction | IsSelf]
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = ('author__uuid',)
    search_fields = ('title', 'category__title')
    ordering_fields = ('title',)
    ordering = ('-created',)


class PostPhotosViewSet(viewsets.ModelViewSet):
    queryset = PostPhoto.objects.all()
    serializer_class = PostPhotoSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    related_model = Post
