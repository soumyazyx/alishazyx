from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse


@twilio_view
def dummy(request):
    r = MessagingResponse()
    r.message("Thanks for the SMS message!")
    return r
