from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("products/<str:categoryname>", views.show_products),
]
