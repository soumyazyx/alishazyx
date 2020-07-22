from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

import hello.views

urlpatterns = [
    path("", include("frontend.urls")),
    path("api/", include("hello.urls")),
    path("bot/", include("bot.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path("", hello.views.index, name="index"),

# path('', include('frontend.urls')),
# path('api/', include('api.urls')),
# path('accounts/', include('allauth.urls')),
# path('admin/', admin.site.urls),
