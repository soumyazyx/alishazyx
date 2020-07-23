from django_twilio.decorators import twilio_view
from django.core.files import File  # you need this somewhere
import urllib.request
from twilio.twiml.messaging_response import MessagingResponse
from hello.models import DemoImage
import requests
import os
import json


@twilio_view
def dummy(request):

    # url = "https://upload.wikimedia.org/wikipedia/commons/b/b1/John_Leak_P02939.jpg"
    # result = urllib.request.urlretrieve(url)
    # reopen = open(result[0], "rb")
    # django_file = File(reopen)
    # demoimg = DemoImage()
    # demoimg.title = "title"
    # demoimg.image.save("logo.png", django_file, save=True)

    name = request.POST.get("Body", "")
    sid = request.POST.get("MessageSid", "")
    print("TIU-SID")
    print(sid)
    MediaUrl0 = request.POST.get("MediaUrl0")
    print("TIU-MediaUrl0")
    print(MediaUrl0)
    print("---")
    if MediaUrl0:
        result = urllib.request.urlretrieve(MediaUrl0)
        reopen = open(result[0], "rb")
        django_file = File(reopen)
        demoimg = DemoImage()
        demoimg.title = "title"
        demoimg.image.save("logo.png", django_file, save=True)
    else:
        print("No media")
    msg = "{} - {}".format(sid, name)
    r = MessagingResponse()
    r.message(msg)
    return r
