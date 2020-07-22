from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse
import os


@twilio_view
def dummy(request):
    # r = MessagingResponse()
    # r.message("Thanks for the SMS message!")
    # return r

    name = request.POST.get("Body", "")
    msg = "Hey %s, how are you today?" % (name)
    r = MessagingResponse()
    r.message(msg)
    return r

