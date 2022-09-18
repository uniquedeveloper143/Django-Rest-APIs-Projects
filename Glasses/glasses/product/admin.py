from django.contrib import admin

# Register your models here.
from django.contrib.admin import TabularInline

from glasses.product.models import ProductPhoto, Product


class ProductPhotoInline(TabularInline):
    model = ProductPhoto
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )
    inlines = (ProductPhotoInline, )


admin.site.register(Product, ProductAdmin)

