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
from lib.bot.bot_utils import (
    save_telegram_message,
    scan_messages,
    send_message,
    get_categories,
)
from rest_framework import status
from rest_framework.response import Response
from twilio.twiml.messaging_response import MessagingResponse

from bot.models import TelegramMessage
from hello.models import Category, DemoImage


def scan(request):
    scan_messages()
    return HttpResponse("ok", status=status.HTTP_200_OK)


@csrf_exempt
def telegram_handler(request):

    print("Message received from telegram..")
    message = request.body.decode("utf-8")
    body_json = json.loads(message)
    update_id = body_json["update_id"]
    chat_id = body_json["message"]["chat"]["id"]
    if "text" in body_json["message"]:
        text = body_json["message"]["text"]
    else:
        text = ""
    print("Saving message to DB..")
    save_telegram_message_res = save_telegram_message(
        json_msg=message, update_id=update_id
    )
    if save_telegram_message_res == -1:
        print("Saving message to DB..FAILED!")
        return HttpResponse(status=400)
    else:
        print("Saving message to DB..Done [id={}]".format(
            save_telegram_message_res))

    if text.lower() == "startzyx":
        send_message(chat_id, get_categories())
    elif text.lower() == "endzyx":
        scan_messages()
    return HttpResponse("ok", status=200)
