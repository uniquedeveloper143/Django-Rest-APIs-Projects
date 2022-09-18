from django.contrib import admin

from blogs.category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    readonly_fields = ('slug',)
