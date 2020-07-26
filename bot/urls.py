from django.urls import path
from . import views

urlpatterns = [path("", views.telegram_handler), path("scan/", views.scan)]
