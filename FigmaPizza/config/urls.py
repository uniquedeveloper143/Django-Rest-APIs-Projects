from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('custom_auth/', include('figma_pizza.custom_auth.api_urls')),
        path('registration/', include('figma_pizza.registrations.api_urls')),
        path('product/', include('figma_pizza.product.api_urls')),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
