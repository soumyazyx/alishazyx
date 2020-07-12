from django.shortcuts import render
from hello.models import Category, Product


def index(request):

    categories = Category.objects.all()
    products = Product.objects.all()
    print(categories)
    for category in categories:
        print(category.id)
        print(category.name)
        print(category.desc)
        print(category.created_on)
    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, "index.html", context)

