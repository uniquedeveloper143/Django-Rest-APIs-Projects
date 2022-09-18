from django.contrib import admin

from f_hlis.post.models import Category, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
