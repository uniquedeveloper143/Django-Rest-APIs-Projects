from django.contrib import admin

# Register your models here.
from glasses.category.models import Category, SubCategory


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


class SubCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


admin.site.register(Category, CategoryAdmin)

admin.site.register(SubCategory, SubCategoryAdmin)
