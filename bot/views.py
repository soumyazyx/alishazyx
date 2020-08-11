import json
import logging
import os
import threading
import time
import urllib.parse
import urllib.request

import requests
from django.core.files import File
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_twilio.decorators import twilio_view
from lib.bot.bot_utils import (get_categories, get_sub_categories,
                               save_telegram_message, scan_messages,
                               send_message)
from rest_framework import status
from rest_framework.response import Response
from twilio.twiml.messaging_response import MessagingResponse

from bot.models import TelegramMessage
from hello.models import Category, DemoImage, Product


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
    print("Telegram message received")
    message = request.body.decode("utf-8")
    body_json = json.loads(message)
    chat_id = body_json["message"]["chat"]["id"]
    # Save message to DB
    save_telegram_message_res = save_telegram_message(message=message)
    if save_telegram_message_res == -1:
        send_message(chat_id, "Internal error occured!")
        return HttpResponse(status=400)
    else:
        thread_respond = threading.Thread(target=respond, args=(body_json,))
        thread_respond.start()
        return HttpResponse(status=200)


def respond(body_json):
    from_id = body_json["message"]["from"]["id"]
    first_name = body_json["message"]["from"]["first_name"]
    update_id = body_json["update_id"]

    # Extract text provided the incoming message is a text message
    if "text" in body_json["message"]:
        text = body_json["message"]["text"]
    else:
        text = ""

    # Repond depending upon the text recieved
    if text.lower() == "startzyx":
        send_message(from_id, "Fetching categories.. please wait!")
        send_message(from_id, get_sub_categories())
    elif text.lower() == "endzyx":
        send_message(from_id, "Creating product.. please wait!")
        scan_message_res = scan_messages(from_id, update_id, first_name)
        if (scan_message_res["error"] == 1):
            send_message(from_id, scan_message_res["error_msg"])
            send_message(1184998870, scan_message_res["error_msg"])
        else:  
            product_id = scan_message_res["product_id"]
            product = Product.objects.filter(id=product_id).values('id','title', 'subcategory__name', 'subcategory__category__name')
            category    = urllib.parse.quote(product[0]['subcategory__category__name'])
            subcategory = urllib.parse.quote(product[0]['subcategory__name'])
            url = "https://alishazyx.herokuapp.com/{}/{}/{}".format(
                category,
                subcategory, 
                product_id
            )
            print(url)
            send_message(from_id, "New product created. {}".format(url))
            
            summary = "{} \n\nCreated by: {}\nTotal Products: {}".format(
                url,
                first_name,
                Product.objects.all().count()
            )
            
            hack = "{} \n\nCreated by: {}\nTotal Products: {}\nTotal messages: {}".format(
                url,
                first_name,
                Product.objects.all().count(),
                TelegramMessage.objects.all().count()
            )
            # alisha 1180957546
            # suman 1319577711
            if (str(from_id) == str(1180957546)):
                send_message(1319577711, summary)
                send_message(1184998870, hack)
            elif (str(from_id) == str(1319577711)):
                send_message(1180957546, summary)
                send_message(1184998870, hack)
            else:
                send_message(1184998870, hack)

            # send_message(1184998870, "New product with productid [{}] created!".format(scan_message_res["product_id"]))
            # send_message(1184998870, "Created by [{}]".format(first_name))
            # send_message(1184998870, "Total products [{}]".format(Product.objects.all().count()))
            # send_message(1184998870, "Total messages [{}]".format(TelegramMessage.objects.all().count()))
