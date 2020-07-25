import json
import logging
import os
import urllib.request

import requests
from django.core.files import File
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse

from bot.models import TelegramMessage
from hello.models import Category, DemoImage
from lib.bot.bot_utils import save_telegram_message


@csrf_exempt
def telegram_handler(request):

    print("Message received from telegram..")
    received_json_data = json.loads(request.body)
    print("Saving message to DB..")
    save_telegram_message_res = save_telegram_message(received_json_data)
    if save_telegram_message_res == -1:
        print("Saving message to DB..FAILED!")
        return HttpResponse(status=400)
    else:
        print("Saving message to DB..Done [id={}]".format(save_telegram_message_res))
        return HttpResponse("ok", status=200)

    # someurl = "https://api.telegram.org/bot1220904092:AAFa_l0w-ycsnldjLpk_noalgGRk0g0PMJo/getUpdates"
    # r = requests.get(someurl)
    # print(r.json())
    # imgurl = "https://api.telegram.org/file/bot1220904092:AAFa_l0w-ycsnldjLpk_noalgGRk0g0PMJo/photos/file_1.jpg"
    # opener = urllib.request.build_opener()
    # opener.addheaders = [("User-agent", "Mozilla/5.0")]
    # urllib.request.install_opener(opener)
    # result = urllib.request.urlretrieve(imgurl)
    # reopen = open(result[0], "rb")
    # django_file = File(reopen)
    # demoimg = DemoImage()
    # demoimg.title = "telegram-1"
    # demoimg.image.save("telegram.png", django_file, save=True)


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
