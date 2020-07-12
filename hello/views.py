from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Product, Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers


def apiOverview(request):
    api_urls = {
        "Categories": "/categories/",
        "Products": "/products/categoryid",
    }
    return JsonResponse(api_urls)


def categories(request):
    qs = Category.objects.all()
    qs_json = serializers.serialize("json", qs)
    return HttpResponse(qs_json, content_type="application/json")


def products(request, categoryid):
    products_qs = Product.objects.filter(product_category_id=categoryid).order_by("-id")
    products_qs_json = serializers.serialize("json", products_qs)
    return HttpResponse(products_qs_json, content_type="application/json")
