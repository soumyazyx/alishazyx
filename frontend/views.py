import re
import json
import time
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from contextlib import suppress
from django.core import serializers
from hello.models import Category, SubCategory, Product, ProductImage


def index(request):
    category_qs = Category.objects.all()
    return render(request, "frontend/index.html", {"categories": category_qs})


def sub_category_view(request, categoryname):
    subcategories_qs = SubCategory.objects.filter(category__name=categoryname).order_by("sequence")
    return render(
        request, "frontend/subcategory.html", {"subcategories": subcategories_qs, "category_name": categoryname},
    )


def products_view(request, categoryname, subcategoryname):
    subcategory = SubCategory.objects.filter(category__name=categoryname).filter(name=subcategoryname).first()
    prds = Product.objects.filter(subcategory=subcategory).order_by("-created_on")
    products = {}
    for product in prds:
        product_id = product.id
        products[product_id] = {}
        products[product_id]["sku"] = product.sku
        products[product_id]["title"] = product.title
        products[product_id]["description"] = product.description
        products[product_id]["images"] = []
        products[product_id]["images"].append(product.coverimage.url)
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

    product = get_object_or_404(Product, id=productid)
    product_details = {}
    product_details["sku"] = product.sku
    product_details["title"] = product.title
    product_details["coverimage"] = transform_url(product.cover_img_url)
    product_details["description"] = product.description
    # Handle additional images
    # During initial implementation, we added each image as a record in ProductImage table.
    # however, we have a 10K record limit imposed by heroku - so, we then started adding image colomns in Product table ieself
    # So, for backward compatibility, we need to pull images from Product table, as well as ProductImage table
    product_details["images"] = []
    # 1. Pull images from ProductImage table
    photos = list(ProductImage.objects.filter(product=product))
    for photo in photos:
        product_details["images"].append(transform_url(photo.image.url))
    # 2. Pull images from product table,. the columns are named as additional_image_1 through additional_image_50
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_1.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_2.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_3.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_4.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_5.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_6.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_7.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_8.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_9.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_10.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_11.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_12.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_13.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_14.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_15.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_16.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_17.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_18.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_19.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_20.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_21.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_22.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_23.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_24.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_25.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_26.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_27.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_28.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_29.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_30.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_31.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_32.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_33.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_34.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_35.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_36.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_37.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_38.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_39.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_40.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_41.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_42.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_43.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_44.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_45.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_46.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_47.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_48.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_49.url))
    with suppress(ValueError):product_details["images"].append(transform_url(product.additional_image_50.url))

    return render(
        request,
        "frontend/product.html",
        {
            "productid": productid,
            "category": categoryname,
            "subcategory": subcategoryname,
            "product_details": product_details,
        },
    )


def transform_url(original_url):
    # transformed_image_url = re.sub(
    #     r"(https://res.cloudinary.com/hxjbk5wno/image/upload/)..(.*?)",
    #     r"\1h_520,w_440,c_pad,b_auto\2",
    #     original_url
    # )

    # transformed_image_url = re.sub(
    #     r"(https://res.cloudinary.com/hxjbk5wno/image/upload/)..(.*?)", r"\1ar_3:4,c_pad,b_auto\2", original_url
    # )
    transformed_image_url = re.sub(
        r"(https://res.cloudinary.com/hxjbk5wno/image/upload/)..(.*?)", r"\1ar_3:4,c_pad\2", original_url
    )

    # (https:\/\/res\.cloudinary\.com\/hxjbk5wno\/image\/upload\/)(v.*?)\/(.*)
    # ar_3:4,c_fill_pad,g_auto,b_auto
    return transformed_image_url
