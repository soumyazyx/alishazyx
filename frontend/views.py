import json
import time
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404

from hello.models import Category, SubCategory, Product, ProductImage


def index(request):
    # get all categories
    category_qs = Category.objects.all()
    # category_json = json.load(serializers.serialize("json", category_qs))
    return render(request, "frontend/index.html", {"categories": category_qs})


def product_view(request, categoryname):
    start = time.time()
    subcategories = list(SubCategory.objects.filter(category__name=categoryname))
    products = {}
    for subcategory in subcategories:
        subcategory_name = subcategory.name
        products[subcategory_name] = {}
        prds = list(Product.objects.filter(subcategory=subcategory).order_by("id"))
        for product in prds:
            product_id = product.id
            products[subcategory_name][product_id] = {}
            products[subcategory_name][product_id]["sku"] = product.sku
            products[subcategory_name][product_id]["title"] = product.title
            products[subcategory_name][product_id]["description"] = product.description
            products[subcategory_name][product_id]["images"] = []
            products[subcategory_name][product_id]["images"].append(product.image.url)
            photos = list(ProductImage.objects.filter(product=product))
            for photo in photos:
                products[subcategory_name][product_id]["images"].append(photo.image.url)
    return render(
        request,
        "frontend/products.html",
        {"products_details": products, "subcategories_count": len(products)},
    )


def detail_view(request, id):
    product = get_object_or_404(Product, id=id)
    photos = ProductImage.objects.filter(product=product)
    return render(request, "details.html", {"product": product, "photos": photos})


def fashi(request):
    return render(request, "frontend/index_fashi.html")


def login(request):
    return render(request, "frontend/login.html")
