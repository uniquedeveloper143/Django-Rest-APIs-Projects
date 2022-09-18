from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from f_hlis.post.models import Post, Like, Comment
from f_hlis.post.serializers import PostSerializer, LikeSerializer, CommentSerializer, PhotoSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    serializer_class = PostSerializer
    # lookup_field = 'id'

    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated, IsAdminUser], url_path='post_photo')
    def post_photo(self, request, *args, **kwargs):
        post = self.get_object()
        # serializer = self.get_serializer(self.request.user, data=self.request.data)

        serializer = PhotoSerializer(post, data=self.request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # data = serializer.validated_data
        # # data.update({'post': post})
        # # print('sagfsdagfs',data.update({'post': post}))
        # print(data)
        serializer.save()
        print(request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    serializer_class = LikeSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    serializer_class = CommentSerializer


