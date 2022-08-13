import os


from twilio.rest import Client

from constants import numbers

import math
from datetime import timedelta
from functools import lru_cache

import boto3

from botocore.exceptions import ClientError


def make_call():
    origination_number = os.getenv("ORIG_NUMBER")
    destination_numbers = [os.getenv("DEST_NUMBER")]

    language_code = "en-US"
    voice_id = "Kendra"
    ssml_message = "<speak>Appointment available</speak>"

    sms_voice_client = boto3.client("pinpoint-sms-voice", region_name="eu-west-1")

    for destination_number in destination_numbers:
        print(
            f"Sending voice message from {origination_number} to {destination_number}."
        )

        try:
            sms_voice_client.send_voice_message(
                DestinationPhoneNumber=destination_number,
                OriginationPhoneNumber=origination_number,
                Content={
                    "SSMLMessage": {
                        "LanguageCode": language_code,
                        "VoiceId": voice_id,
                        "Text": ssml_message,
                    }
                },
            )
        except ClientError:
            print(
                f"Couldn't send message from {origination_number} to {destination_number}."
            )

        print("Message sent!")

