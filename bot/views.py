from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def dummy(request):
    twiml = "<Response><Message>Hello from your Django app!</Message></Response>"
    return HttpResponse(twiml, content_type="text/xml")
