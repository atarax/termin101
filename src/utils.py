import os

from twilio.rest import Client

from constants import numbers


def makeCall(name="yilmaz"):

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]

    number = numbers[name]
    client = Client(account_sid, auth_token)

    call = client.calls.create(to=number, from_="+17029450859", url="http://demo.twilio.com/docs/voice.xml")

    print(call.sid)
