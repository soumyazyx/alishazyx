import json
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404

from hello.models import Category, Product, ProductImage


def index(request):
    # get all categories
    category_qs = Category.objects.all()
    # category_json = json.load(serializers.serialize("json", category_qs))
    return render(request, "frontend/index.html", {"categories": category_qs})


def product_view(request, categoryname):
    category = get_object_or_404(Category, name=categoryname)
    products = Product.objects.filter(category=category)
    return render(
        request,
        "frontend/products.html",
        {"products": products, "category": categoryname},
    )


def detail_view(request, categoryname, id):
    product = get_object_or_404(Product, id=id)
    photos = ProductImage.objects.filter(product=product)
    return render(request, "details.html", {"product": product, "photos": photos})


def fashi(request):
    return render(request, "frontend/index_fashi.html")
