from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting, imggal

# Create your views here.
def index(request):
    results = imggal.objects.all()
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html", {"imggal": results})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
