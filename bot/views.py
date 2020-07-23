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
    print(request)  #  <WSGIRequest: POST '/bot/'>
    print(
        request.body
    )  # b'MediaContentType0=image%2Fjpeg&SmsMessageSid=MM33a247a129f11937eccd9b170ad9965e&NumMedia=1&SmsSid=MM33a247a129f11937eccd9b170ad9965e&SmsStatus=received&Body=&To=whatsapp%3A%2B14155238886&NumSegments=1&MessageSid=MM33a247a129f11937eccd9b170ad9965e&AccountSid=ACb1b6171834a4de554bd3f43d8488b969&From=whatsapp%3A%2B919553884727&MediaUrl0=https%3A%2F%2Fapi.twilio.com%2F2010-04-01%2FAccounts%2FACb1b6171834a4de554bd3f43d8488b969%2FMessages%2FMM33a247a129f11937eccd9b170ad9965e%2FMedia%2FME89dec689478af38927f9c5ffd1e87a32&ApiVersion=2010-04-01'
    print(
        body_unicode
    )  # MediaContentType0=image%2Fjpeg&SmsMessageSid=MM33a247a129f11937eccd9b170ad9965e&NumMedia=1&SmsSid=MM33a247a129f11937eccd9b170ad9965e&SmsStatus=received&Body=&To=whatsapp%3A%2B14155238886&NumSegments=1&MessageSid=MM33a247a129f11937eccd9b170ad9965e&AccountSid=ACb1b6171834a4de554bd3f43d8488b969&From=whatsapp%3A%2B919553884727&MediaUrl0=https%3A%2F%2Fapi.twilio.com%2F2010-04-01%2FAccounts%2FACb1b6171834a4de554bd3f43d8488b969%2FMessages%2FMM33a247a129f11937eccd9b170ad9965e%2FMedia%2FME89dec689478af38927f9c5ffd1e87a32&ApiVersion=2010-04-01
    print(
        request.POST
    )  # <QueryDict: {'MediaContentType0': ['image/jpeg'], 'SmsMessageSid': ['MM33a247a129f11937eccd9b170ad9965e'], 'NumMedia': ['1'], 'SmsSid': ['MM33a247a129f11937eccd9b170ad9965e'], 'SmsStatus': ['received'], 'Body': [''], 'To': ['whatsapp:+14155238886'], 'NumSegments': ['1'], 'MessageSid': ['MM33a247a129f11937eccd9b170ad9965e'], 'AccountSid': ['ACb1b6171834a4de554bd3f43d8488b969'], 'From': ['whatsapp:+919553884727'], 'MediaUrl0': ['https://api.twilio.com/2010-04-01/Accounts/ACb1b6171834a4de554bd3f43d8488b969/Messages/MM33a247a129f11937eccd9b170ad9965e/Media/ME89dec689478af38927f9c5ffd1e87a32'], 'ApiVersion': ['2010-04-01']}>
    print("\nTIU-BODY")
    print(request.POST.get("Body", ""))
    print("\nTIU-MessageSid")
    print(request.POST.get("MessageSid", ""))
    print("\nTIU-MediaUrl0")
    print(request.POST.get("MediaUrl0", ""))
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
    sid = request.POST.get("MessageSid", "")
    msg = "{} - {}".format(sid, name)
    print(msg)
    r = MessagingResponse()
    r.message(msg)
    return r
