from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("login/", views.login),
    path("fashi/", views.fashi),
    path("products/<str:categoryname>", views.product_view),
    path("products/<str:categoryname>/<str:id>", views.detail_view),
]
