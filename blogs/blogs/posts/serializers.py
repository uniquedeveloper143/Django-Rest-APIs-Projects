from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from blogs.category.serializers import CategorySerializer
from blogs.custom_auth.serializers import BaseUserSerializer
from blogs.posts.models import Post, PostPhoto


class PostPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPhoto
        fields = ('id', 'image', 'width', 'height',)

        _required = {'required': True}
        _not_required = {'required': False}
        extra_kwargs = {
            'image': _required,
            'width': _not_required,
            'height': _not_required,
        }

    def create(self, validated_data):
        images = dict(self.context['request'].data)['image']
        if len(images) and images[0] == '':
            raise ValidationError(_("Images filed is required."))
        bulk_images = [
            PostPhoto(post_id=self.context['view'].kwargs.get('nested_1_pk'), image=images[i])
            for i in range(len(images))
        ]
        return PostPhoto.objects.bulk_create(bulk_images)[0]


class PostSerializer(serializers.ModelSerializer):
    author = BaseUserSerializer(read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    photos = PostPhotoSerializer(source='post_photos', read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'content', 'author', 'category', 'category_detail', 'published', 'photos',)

    def create(self, validated_data):
        validated_data['category'] = validated_data.pop('category', None)
        validated_data['author'] = self.context['request'].user
        validated_data['published'] = True
        return super().create(validated_data)
