"""Python module that manages the emails for the app.

It uses SendinBlue API as documented here : https://developers.sendinblue.com/reference

"""
import csv
import io
import json
import logging
import re
from datetime import datetime, date
from typing import Dict, Iterable, Tuple, List

import requests
from django.db import transaction
from django.utils import timezone
from sentry_sdk import capture_exception

from appel_crises.models import Signature
from appel_crises import settings

SB_HEADER = {'api-key': settings.SENDIN_BLUE_API_KEY}

SB_SEND_MAIL_URL = "https://api.sendinblue.com/v3/smtp/email"
SB_IMPORT_CONTACTS_URL = "https://api.sendinblue.com/v3/contacts/import"
SB_FETCH_EVENTS_URL = "https://api.sendinblue.com/v3/smtp/statistics/events"
NEWSLETTER_LIST_ID = 19

logger = logging.getLogger(__name__)

MailingPerson = Dict[str, str]
DeliveryResult = Tuple[str, datetime]


def format_text_for_email(text: str) -> str:
    """
    Format the text correctly so it can be pretty in mailers.

    For example:
    >>> text = chr(10).join("Hello,", "", "My name is Hadrien.", "Bye")
    >>> format_text_for_email(text)
    '<div>Hello,</div><div><br></div><div>My name is Hadrien.</div><div>Bye</div>'

    Furthermore, it replaces the every word `appel` (matched case-insensitve) by a
    link to the home page. For example:
    >>> settings.MAIN_URL = "https://test.fr"
    >>> text = "Je vous rappelle pour soutenir l'appel."
    >>> format_text_for_email(text)
    '<div>Je vous rappelle pour soutenir l\'<a href="https://test.fr">appel</a>.</div>'

    :param text: a string, as returned by the browser
    :return: a string, prettyfied with html tags
    """

    # Replace the words `appel` by the links
    text = re.sub(
        r"(?P<pre>\W)(?P<content>appel)(?P<post>\W)",
        r'\g<pre><a href="' + settings.MAIN_URL + r'">\g<content></a>\g<post>',
        text,
        flags=re.I,
    )

    # Replace new lines characters by divs and <br> if needed
    raw_lines = text.split("\n")
    beautified_lines = ""

    for i, line in enumerate(raw_lines):
        if re.fullmatch(r"\s*", line):
            if i == 0 or i == len(raw_lines) - 1:
                continue
            line = "<br>"
        line = "<div>" + line + "</div>"
        beautified_lines += line

    return beautified_lines


def mailing_person(email: str, name: str = None) -> MailingPerson:
    """Build a MailingPerson dict."""
    if name is not None:
        return dict(name=name, email=email)
    else:
        return dict(email=email)


def send_and_save(payload: Dict, instance: object) -> bool:
    """
    Send mail and mark instance as sent

    :param payload: the mail to send
    :param instance: The instance of the model
    :return: True if the sending was successful
    """
    with transaction.atomic():
        # Reload and lock instance (from the database)
        instance = instance.__class__.objects.select_for_update().get(pk=instance.pk)
        # Instance might have been sent while we were waiting for a lock
        if not instance.email_sent_at:
            try:
                response = requests.post(
                    SB_SEND_MAIL_URL, json=payload, headers=SB_HEADER
                )
                response.raise_for_status()
            except Exception as e:
                # No action taken on failure; invalid mails will be
                # retried ad infinitum.
                logger.error("Invalid response on POST to send mail: %r", e)
                logger.error("Associated response text: %s", response.text)
                capture_exception(e)
                return False
            else:
                logger.debug("Mail to %r sent successfully", payload['to'])

                instance.email_sent_at = timezone.now()
                instance.save()

                return True

        return False


def send_mail(
    instance: object,
    sender: MailingPerson,
    to: Iterable[MailingPerson],
    subject: str,
    text: str = "",
    bcc: Iterable[MailingPerson] = None,
    cc: Iterable[MailingPerson] = None,
) -> bool:
    """Uses SendinBlue API to send an email"""

    payload = dict(
        sender=sender,
        to=to,
        htmlContent=format_text_for_email(text),
        textContent=text,
        subject=subject,
    )

    if bcc is not None:
        payload['bcc'] = bcc

    if cc is not None:
        payload['cc'] = cc

    return send_and_save(payload=payload, instance=instance)


def send_template(
    instance: object,
    template_id: int,
    to: Iterable[MailingPerson],
    bcc: Iterable[MailingPerson] = None,
    cc: Iterable[MailingPerson] = None,
) -> bool:
    """Uses SendinBlue API to send an email from a template"""

    payload = dict(to=to, templateId=template_id)

    if bcc is not None:
        payload['bcc'] = bcc

    if cc is not None:
        payload['cc'] = cc

    return send_and_save(payload=payload, instance=instance)


def get_delivered_emails(offset: int, limit: int = 100) -> List[DeliveryResult]:
    """Fetch the delivered emails."""
    params = dict(offset=offset, limit=limit, event="delivered")

    try:
        resp = requests.get(SB_FETCH_EVENTS_URL, params=params, headers=SB_HEADER)
        data = resp.json()
    except Exception as e:
        capture_exception(e)
        logger.error("Invalid response on GET to fetch delivered emails: %r", e)
        return []

    if 'events' not in data:
        return []

    result = [(e['email'], datetime.fromisoformat(e['date'])) for e in data['events']]

    return result


def build_file_body(signatures: Iterable[Signature]):
    """Build CSV file body for SendInBlue API."""
    # db field -> newsletter list field
    fields_mapping = {
        "email": "EMAIL",
        "first_name": "PRENOM",
        "surname": "NOM",
    }
    added_time = date.today().strftime('%d-%m-%Y')
    db_fields = list(fields_mapping)

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_ALL)
    # header
    writer.writerow([fields_mapping[field] for field in db_fields] + ["ADDED_TIME"])

    # body
    for signature in signatures:
        writer.writerow(
            [getattr(signature, field) for field in db_fields] + [added_time]
        )

    output.seek(0)
    return output.read()


def add_signatures_to_newsletter_list(signatures: Iterable[Signature]):
    """Add emails from signatures and metadata to a newsletter list."""
    payload = {
        "listIds": [NEWSLETTER_LIST_ID],
        "fileBody": build_file_body(signatures),
        "emailBlacklist": False,
        "smsBlacklist": False,
        "updateExistingContacts": False,
        "emptyContactsAttributes": False,
    }
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'api-key': settings.SENDIN_BLUE_API_KEY,
    }

    try:
        response = requests.post(
            SB_IMPORT_CONTACTS_URL, data=json.dumps(payload), headers=headers
        )
        response.raise_for_status()
    except Exception as e:
        capture_exception(e)
        logger.error("Invalid response on POST to add emails to newsletter: %r", e)
        return None

    return response
