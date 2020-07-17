import json

from django.core import serializers
from django.shortcuts import render, get_object_or_404

from hello.models import Category, Product, ProductImage


def index(request):
    # get all categories
    category_qs = Category.objects.all()
    # category_json = json.load(serializers.serialize("json", category_qs))
    return render(request, "frontend/index.html", {"categories": category_qs})


def product_view(request, categoryname):
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


def detail_view(request, categoryname, id):
    product = get_object_or_404(Product, id=id)
    photos = ProductImage.objects.filter(product=product)
    return render(request, "details.html", {"product": product, "photos": photos})


def fashi(request):
    return render(request, "frontend/index_fashi.html")
