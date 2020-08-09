from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.apiOverview),
    path("categories/", views.categories),
    # path("products/<str:categoryname>", views.products),
]
