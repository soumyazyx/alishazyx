import json
import logging
import os
import threading
import time
import urllib.request

import requests
from django.core.files import File
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_twilio.decorators import twilio_view
from lib.bot.bot_utils import (get_categories, save_telegram_message,
                               scan_messages, send_message)
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

    print("Telegram message received")
    # Extract details from message
    message    = request.body.decode("utf-8")
    body_json  = json.loads(message)
    chat_id    = body_json["message"]["chat"]["id"]
    first_name = body_json["message"]["chat"]["first_name"]
    # Save message to DB
    save_telegram_message_res = save_telegram_message(message=message)
    if save_telegram_message_res == -1:
        return HttpResponse(status=400)
    else:
        thread_respond = threading.Thread(target=respond, args=(message,)); thread_respond.start()
        return HttpResponse(status=200)
    

def respond(message):
    body_json = json.loads(message)
    chat_id   = body_json["message"]["chat"]["id"]
    # Extract text provided the incoming message is a text message        
    if "text" in body_json["message"]:
        text = body_json["message"]["text"]
    else:
        text = ""
    
    if text.lower() == "startzyx":
        send_message(chat_id, get_categories())
    elif text.lower() == "endzyx":
        scan_messages()
    
        
    