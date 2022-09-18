from django.contrib import admin

from vendor.custom_auth.models import ApplicationUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'user_type')


admin.site.register(ApplicationUser, UserAdmin)
