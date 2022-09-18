from django.contrib import admin

from ecommerce.product.models import Product,ProductPhoto

from django.contrib.admin import TabularInline


class ProductPhotoInline(TabularInline):
    model = ProductPhoto
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )
    inlines = (ProductPhotoInline, )


admin.site.register(Product, ProductAdmin)
