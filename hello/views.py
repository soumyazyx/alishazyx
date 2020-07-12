from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def index(request):
    results = Product.objects.all()
    return render(request, "index.html", {"products": results})
