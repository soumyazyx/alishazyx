from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

import hello.views

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
