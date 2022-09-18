from django.contrib import admin
from django.contrib.admin import TabularInline

from blogs.posts.models import Post, PostPhoto


class PostPhotosInline(TabularInline):
    model = PostPhoto
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'category', 'published',)
    readonly_fields = ('slug',)
    inlines = (PostPhotosInline,)
