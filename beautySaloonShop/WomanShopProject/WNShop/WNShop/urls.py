from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path
import shop.urls
import cart.urls
from WNShop import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(shop.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)