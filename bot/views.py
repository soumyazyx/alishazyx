from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse
import os
import json


@twilio_view
def dummy(request):
    # r = MessagingResponse()
    # r.message("Thanks for the SMS message!")
    # return r
    print("TIU1")
    # print(">>>>")
    # body_unicode = request.body.decode("utf-8")
    # print(body_unicode)
    # print(">>>>")
    # body = json.loads(body_unicode)
    # print(body)
    # print(">>>>")
    # content = body["content"]
    # print(content)
    print(">>>>")
    body = json.loads(request.body)
    print(body)
    print(">>>>")
    print(body["content"])
    print(">>>>")
    name = request.POST.get("Body", "")
    print(name)
    print(">>>>")
    msg = "%s" % (name)
    print(name)
    print(">>>>")

    r = MessagingResponse()
    r.message(msg)
    return r

