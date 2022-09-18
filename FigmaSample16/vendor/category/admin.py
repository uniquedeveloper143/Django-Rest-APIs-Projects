from django.contrib import admin

from vendor.category.models import Category, City, Shop, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('city',)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
