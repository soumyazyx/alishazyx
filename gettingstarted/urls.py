from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = [
    path("", include("frontend.urls")),
    path("api/", include("hello.urls")),
    path("bot/", include("bot.urls")),
    path("admin/", admin.site.urls),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
