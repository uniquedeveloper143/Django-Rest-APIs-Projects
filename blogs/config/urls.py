"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blogs.custom_auth import web

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('custom-auth/', include('blogs.custom_auth.api_urls')),
        path('registration/', include('blogs.registrations.api_urls')),
        path('category/', include('blogs.category.api_urls')),
        path('posts/', include('blogs.posts.api_urls')),
    ])),
    path('forgot-password/<password_reset_id>', web.password_reset_change_password, name="forgot-password"),
    path('forgot-password-success/', web.password_reset_success, name="forgot-password-success")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)