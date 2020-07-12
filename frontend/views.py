import json

from django.core import serializers
from django.shortcuts import render

from hello.models import Category, Product


def index(request):
    return render(request, "index.html")


def show_products(request, categoryname):
    # get category id from category name
    category_qs = Category.objects.filter(name__iexact=categoryname)
    # Check if we have any product/s for the given category
    if len(category_qs) > 0:
        category_qs_json = json.loads(serializers.serialize("json", category_qs))
        category_id = category_qs_json[0]["pk"]
        # Filter products based on category id
        products = Product.objects.filter(product_category_id=category_id)
        return render(request, "products.html", {"products": products})
    else:
        return render(request, "products.html")
