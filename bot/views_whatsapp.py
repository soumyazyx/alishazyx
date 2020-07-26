import json
import logging
import os
import time
import urllib.request

import requests
from django.core.files import File
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_twilio.decorators import twilio_view
from lib.bot.bot_utils import save_telegram_message, scan_messages
from rest_framework import status
from rest_framework.response import Response
from twilio.twiml.messaging_response import MessagingResponse

from bot.models import TelegramMessage
from hello.models import Category, DemoImage


class ResponseThen(Response):
    def __init__(self, data, then_callback, **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback

    def close(self):
        super().close()
        self.then_callback()


def scan(request):
    scan_messages()
    return HttpResponse("ok", status=status.HTTP_200_OK)


@csrf_exempt
def telegram_handler(request):

    print("Message received from telegram..")
    message = request.body.decode("utf-8")
    body_json = json.loads(message)
    update_id = body_json["update_id"]
    print(update_id)
    if "text" in body_json["message"]:
        text = body_json["message"]["text"]
    else:
        text = ""
    print("Saving message to DB..")
    save_telegram_message_res = save_telegram_message(
        json_msg=message,
        update_id=update_id
    )
    if save_telegram_message_res == -1:
        print("Saving message to DB..FAILED!")
        return HttpResponse(status=400)
    else:
        print("Saving message to DB..Done [id={}]".format(
            save_telegram_message_res))

        if (text.lower() == "endzyx"):
            scan_messages()
        return HttpResponse("ok", status=200)


@csrf_exempt
def telegram_handler_e(request):

    # ...code to run before response is returned to client
    print("Message received from telegram..")
    received_json_data = json.loads(request.body)
    print("Saving message to DB..")
    save_telegram_message_res = save_telegram_message(received_json_data)
    if save_telegram_message_res == -1:
        print("Saving message to DB..FAILED!")
        # return HttpResponse(status=400)
    else:
        print("Saving message to DB..Done [id={}]".format(
            save_telegram_message_res))
        # return HttpResponse("ok", status=200)

    # ..code to run *after* response is returned to client
    def do_after():
        print("...code to run *after* response is returned to client")
        time.sleep(20)
        print("yay!")

    return ResponseThen("some_data", do_after, status=status.HTTP_200_OK)


@twilio_view
def handler(request):
    print("wow")
    get_categories()
    msg = request.POST.get("Body", "")
    r = MessagingResponse()
    r.message(msg)
    return r


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
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0")]
        urllib.request.install_opener(opener)
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


def get_categories():
    print("get categories")
    categories = Category.objects.all()
    print(categories)
    for category in categories:
        print(category.id)
        print(category.sequence)
        print(category.name)
