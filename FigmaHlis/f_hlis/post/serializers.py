from rest_framework import serializers

from f_hlis.post.models import Post, Like, Comment


class PostSerializer(serializers.ModelSerializer):
    total_comment = serializers.SerializerMethodField()
    total_like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('user', 'category', 'title', 'description', 'tags', 'hash_tag', 'file', 'total_comment', 'total_like')

    def get_total_comment(self, obj):
        data = Comment.objects.filter(post=obj)
        return len(data)

    def get_total_like(self, obj):
        data = Like.objects.filter(post=obj, like="True")
        return len(data)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', "post", "like")

    def create(self, validated_data):
        try:
            like = Like.objects.get(user=validated_data['user'], post=validated_data['post'])
            return super().update(like,validated_data)
        except Like.DoesNotExist:
            return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PhotoSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)

    class Meta:
        model = Post
        fields = ('file',)
