from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse
import os
import json


@twilio_view
def dummy(request):
    # json_data = json.loads(request.body.decode(encoding="UTF-8"))
    # print("Raw Data : %s" % json_data)
    # r = MessagingResponse()
    # r.message("Thanks for the SMS message!")
    # return r
    # print("TIU1")
    # print(">>>>")

    body_unicode = request.body.decode("utf-8")
    print(request)
    print(request.body)
    print(body_unicode)
    print(request.POST)
    print(request.POST.get("Body"))
    # print(">>>>")
    # body = json.loads(body_unicode)
    # print(body)
    # print(">>>>")
    # content = body["content"]
    # print(content)
    # print(">>>>")
    # body = json.loads(request.body)
    # print(body)
    # print(">>>>")
    # print(body["content"])
    # print(">>>>")
    # name = request.POST.get("Body", "")
    # print(name)
    # print(">>>>")
    # msg = "%s" % (name)
    # print(name)
    # print(">>>>")
    # print(request.body)
    # body_json = json.loads(request.body)
    # print(body_json)

    name = request.POST.get("Body", "")
    msg = "%s" % (name)
    print(msg)
    r = MessagingResponse()
    r.message(msg)
    return r
