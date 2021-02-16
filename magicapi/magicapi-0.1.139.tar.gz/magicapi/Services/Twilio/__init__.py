from twilio.rest import Client
import os
from functools import wraps
from magicapi import g

from magicapi.Errors import TwilioException

from twilio.base.exceptions import TwilioRestException

try:
    client = Client(g.settings.twilio_account_sid, g.settings.twilio_auth_token)
except Exception as e:
    print("Twilio SID or AUTH TOKEN not given.")

FROM_NUMBER = os.environ.get("FROM_NUMBER")


def need_twilio_vars(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        twilio_vars = [g.settings.twilio_account_sid, g.settings.twilio_auth_token]
        if None in twilio_vars:
            raise TwilioException(
                message="Not all Twilio credentials found in .env file. Need TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN."
            )
        return f(*args, **kwargs)

    return wrapper


def need_copilot_vars(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        twilio_vars = [g.settings.twilio_messaging_service_sid]
        if None in twilio_vars:
            raise TwilioException(
                message="Not all Twilio co-pilot credentials found in .env file. Need MESSAGING_SERVICE_SID."
            )
        return f(*args, **kwargs)

    return wrapper


@need_twilio_vars
def send_text(to, body, from_number=FROM_NUMBER):
    message = client.messages.create(
        body=body,
        from_=from_number,
        to=to,
    )
    return message.sid


@need_twilio_vars
def send_text_with_copilot(to, body, status_callback=g.settings.twilio_status_callback):
    try:
        message = client.messages.create(
            body=body,
            messaging_service_sid=g.settings.twilio_messaging_service_sid,
            to=to,
            status_callback=status_callback,
        )
        return message.sid
    except TwilioRestException as error:
        print("Twilio error here", error)
        print("*THIS WAS THE ERRORED MESSAGE*", body)
