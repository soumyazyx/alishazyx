from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from twilio.twiml.messaging_response import MessagingResponse


@csrf_exempt
def dummy(request):
    r = MessagingResponse()
    r.message("Hello from your Django app!")
    return HttpResponse(r.toxml(), content_type="text/xml")


def dummy2(request):
    twiml = "<Response><Message>Hello from your Django app!</Message></Response>"
    return HttpResponse(twiml, content_type="text/xml")
