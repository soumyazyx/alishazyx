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
from lib.bot.bot_utils import (
    get_sub_categories,
    save_telegram_message,
    scan_messages,
    send_message,
    scan_image_urls,
)
from rest_framework import status
from rest_framework.response import Response
from twilio.twiml.messaging_response import MessagingResponse

from bot.models import TelegramMessage
from hello.models import Category, Product

allowed_from_ids = [1319577711, 1180957546, 1184998870]  # soumya,sumna,alisha
blocked_from_ids = [666034122]


class ResponseThen(Response):
    def __init__(self, data, then_callback, **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback

    def close(self):
        super().close()
        self.then_callback()


def scan(request):

    for product_id in [35, 36, 37, 38, 40]:
        scan_image_urls(product_id=product_id)
    return HttpResponse("scan")


@csrf_exempt
def telegram_handler(request):

    print("Telegram message received")
    message = request.body.decode("utf-8")
    body_json = json.loads(message)
    chat_id = body_json["message"]["chat"]["id"]
    first_name = body_json["message"]["from"]["first_name"]
    # Dont save if the message is from blocked list
    if chat_id in blocked_from_ids:
        print("Rejecting the message as message is recieved from [{}]".format(first_name))
        return HttpResponse(status=200)
    else:
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
        if scan_message_res["error"] == 1:
            send_message(from_id, scan_message_res["error_msg"])
            send_message(1184998870, scan_message_res["error_msg"])
        else:
            product_id = scan_message_res["product_id"]
            product = Product.objects.filter(id=product_id).values(
                "id", "title", "subcategory__name", "subcategory__category__name",
            )
            category = urllib.parse.quote(product[0]["subcategory__category__name"])
            subcategory = urllib.parse.quote(product[0]["subcategory__name"])
            total_products = Product.objects.all().count()
            total_telegram_msges = TelegramMessage.objects.all().count()

            url = "https://alishazyx.herokuapp.com/{}/{}/{}".format(category, subcategory, product_id)
            summary = "{} \n\nCreated by: {}\nTotal Products: {}".format(url, first_name, total_products)
            details = "{} \n\nCreated by: {}\nTotal Products: {}\nTotal messages: {}".format(
                url, first_name, total_products, total_telegram_msges
            )

            # If from_id=Soumya,don't send message as it is most likely for testing purpose
            if str(from_id) == str(1184998870):
                send_message(1184998870, details)
            else:
                send_message(1319577711, summary)  # suman
                send_message(1180957546, summary)  # alisha
                send_message(1184998870, details)  # soumya
