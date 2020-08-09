import re
import json
import time
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from hello.models import Category, SubCategory, Product, ProductImage


def index(request):
    category_qs = Category.objects.all()
    return render(request, "frontend/index.html", {"categories": category_qs})


def sub_category_view(request, categoryname):
    subcategories_qs = SubCategory.objects.filter(
        category__name=categoryname
    ).order_by("sequence")
    return render(
        request,
        "frontend/subcategory.html",
        {"subcategories": subcategories_qs, "category_name": categoryname},
    )


def products_view(request, categoryname, subcategoryname):
    subcategory = (
        SubCategory.objects.filter(category__name=categoryname)
        .filter(name=subcategoryname)
        .first()
    )
    prds = Product.objects.filter(subcategory=subcategory)
    products = {}
    for product in prds:
        product_id = product.id
        products[product_id] = {}
        products[product_id]["sku"] = product.sku
        products[product_id]["title"] = product.title
        products[product_id]["description"] = product.description
        products[product_id]["images"] = []
        products[product_id]["images"].append(product.image.url)
    return render(
        request,
        "frontend/products.html",
        {
            "categoryname": categoryname,
            "subcategoryname": subcategoryname,
            "products_details": products,
            "subcategories_count": len(products),
        },
    )


def product_view(request, categoryname, subcategoryname, productid):

    original_image_urls = []

    product = get_object_or_404(Product, id=productid)
    product_details = {}
    product_details["sku"] = product.sku
    product_details["title"] = product.title
    product_details["coverimage"] = transform_url(product.image.url)
    product_details["description"] = product.description
    # Handle additional images
    product_details["images"] = []
    photos = list(ProductImage.objects.filter(product=product))
    for photo in photos:
        product_details["images"].append(transform_url(photo.image.url))

    print(product_details)
    # return HttpResponse("wow")
    # return render(
    #     request,
    #     "frontend/product_detail.html",
    #     {"product_details": product_details},
    # )
    return render(
        request, "frontend/product.html", {"product_details": product_details},
    )

def login(request):
    return render(request, "frontend/login.html")

def transform_url(original_url):
    transformed_image_url = re.sub(
        r"(https://res.cloudinary.com/hxjbk5wno/image/upload/)..(.*?)",
        r"\1h_520,w_440,c_pad,b_auto\2",
        original_url
    )
    return transformed_image_url
