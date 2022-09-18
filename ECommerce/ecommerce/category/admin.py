from django.contrib import admin

from ecommerce.category.models import Category


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )


admin.site.register(Category, CategoryAdmin)
