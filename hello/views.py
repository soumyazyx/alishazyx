from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Product, Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
import json


def apiOverview(request):
    api_urls = {
        "Categories": "/categories/",
        "Products": "/products/categoryname",
    }
    return JsonResponse(api_urls)


def categories(request):
    qs = Category.objects.all()
    qs_json = serializers.serialize("json", qs)
    return HttpResponse(qs_json, content_type="application/json")


# def products(request, categoryname):
#     # get category id from category name
#     category_qs = Category.objects.filter(name__iexact=categoryname)
#     category_qs_json = json.loads(serializers.serialize("json", category_qs))
#     category_id = category_qs_json[0]["pk"]
#     # get products based on category id
#     products_qs = Product.objects.filter(product_category_id=category_id).order_by("id")
#     products_qs_json = serializers.serialize("json", products_qs)
#     return HttpResponse(products_qs_json, content_type="application/json")

