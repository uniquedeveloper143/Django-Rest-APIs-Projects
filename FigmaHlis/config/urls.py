from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('custom_auth/', include('f_hlis.custom_auth.api_urls')),
        path('registration/', include('f_hlis.registrations.api_urls')),
        path('post/', include('f_hlis.post.api_urls')),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
