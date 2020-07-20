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
    products_details = {}
    category = get_object_or_404(Category, name=categoryname)
    products = Product.objects.filter(category=category).order_by("id")
    for product in products:
        products_details[product.id] = {}
        products_details[product.id]["sku"] = product.sku
        products_details[product.id]["title"] = product.title
        products_details[product.id]["category"] = product.category
        products_details[product.id]["description"] = product.description
        products_details[product.id]["images"] = []
        products_details[product.id]["images"].append(product.image.url)

        photos_qs = ProductImage.objects.filter(product=product)
        for photo in photos_qs:
            products_details[product.id]["images"].append(photo.image.url)
    print(products_details)
    return render(
        request, "frontend/products.html", {"products_details": products_details},
    )


def detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    photos = ProductImage.objects.filter(product=product)
    return render(request, "details.html", {"product": product, "photos": photos})


def fashi(request):
    return render(request, "frontend/index_fashi.html")
