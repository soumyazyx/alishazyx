from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("<str:categoryname>", views.sub_category_view),
    path("<str:categoryname>/<str:subcategoryname>", views.products_view),
    path("<str:categoryname>/<str:subcategoryname>/<str:productid>", views.product_view),
]
