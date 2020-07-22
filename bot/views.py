from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse


def dummy(request):
    return HttpResponse("hi there!")
