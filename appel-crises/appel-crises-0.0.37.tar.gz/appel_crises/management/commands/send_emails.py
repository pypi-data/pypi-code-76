import random
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Iterable, List, Union

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from . import BaseCommand
from sentry_sdk import capture_message

from appel_crises.data import DISTRICT_TO_MP
from appel_crises.data.gvt import GVT
from appel_crises.mailer import (
    send_mail,
    mailing_person,
    MailingPerson,
    send_template,
)
from appel_crises.models import Signature, CallOutEmail

SendSignature = Union[Signature, type(None)]
SendCallOutEmail = Union[CallOutEmail, type(None)]

if settings.MAILING_CATCHALL and ('{}' not in settings.MAILING_CATCHALL):
    raise ImproperlyConfigured("Missing '{}' in settings.MAILING_CATCHALL")


def get_gvt_address() -> MailingPerson:
    """Returns an address from the government, as specified in data.gvt ."""
    return random.choice(GVT)


def mailing_persons_from_circonscriptions(circo_numbers: str) -> List[MailingPerson]:
    """
    Fetch the list of mailing persons from stored data.

    :param circo_numbers: The circonscription numbers, comma separated,
                          for example: "93.1,75.3"
    :returns: A list of MailingPerson, as the mailer expects it as
              recipients of an email.
    """
    return [
        mailing_person_from_circonscription(number)
        for number in circo_numbers.split(',')
        if len(number) > 0
    ]


def mailing_person_from_circonscription(circo_number: str) -> MailingPerson:
    """
    Match a circonscription number with the associated mp data,
    formatted as the mailer expects it.
    """
    mp = DISTRICT_TO_MP[circo_number]

    if settings.APPMODE != 'prod':
        mailto = "hadrien.renaudlebret@gmail.com"
    else:
        mailto = mp[3]

    return mailing_person(mailto, mp[0])


def maybe_catchall(persons: Iterable[MailingPerson]) -> Iterable[MailingPerson]:
    """
    Edit email addresses to prevent unwanted emails in staging environments.

    It uses settings.MAILING_CATCHALL to replace email addresses.
    For example:
    >>> settings.MAILING_CATCHALL = 'invalid+{}@example.com'
    >>> maybe_catchall(({'name': 'h', 'email': 'h@example.com'},))
    [{'name': 'h', 'email': 'invalid+h_at_example.com@example.com'},]

    :param persons: A list of email recipients to check
    :return: A list of checked email recipients
    """
    if not settings.MAILING_CATCHALL:
        return persons

    return [
        mailing_person(
            name=person.get('name'),
            email=settings.MAILING_CATCHALL.format(
                person['email'].replace('@', '_at_')
            ),
        )
        for person in persons
    ]


class Command(BaseCommand):
    help = "Send emails for all Signature for which it hasn't been done before."

    def handle(self, *args, **options):
        self.send_to_signatures()
        self.send_call_out_emails()

    def send_to_signatures(self):
        """Do the job."""
        start = time.time()

        with ThreadPoolExecutor(max_workers=settings.MAX_THREAD_WORKERS) as executor:
            results = executor.map(
                self.send_one_mail_to_a_signature, list(Signature.get_unsent())
            )

        modified = sum(results)

        stop = time.time()

        self.stdout.write(
            f"Successfully sent {modified} signatures emails " f"in {stop - start:.2}s."
        )

    def send_one_mail_to_a_signature(self, signature: Signature) -> bool:
        """
        Send an email to the corresponding signature.

        :param signature: the recipient of the email
        :return: True if the sending was successful
        """
        name = signature.first_name + " " + signature.surname

        sending_result = send_template(
            to=maybe_catchall([mailing_person(signature.email, name)]),
            template_id=settings.SIGNATURE_TEMPLATE_ID,
            instance=signature,
        )

        if not sending_result:
            self.stderr.write(f"Sending mail to {signature} failed.")
            capture_message(f"Sending mail to {signature} failed")

        return sending_result

    def send_call_out_emails(self):
        """Send the pending emails in CallOutEmail table."""
        start = time.time()

        with ThreadPoolExecutor(max_workers=settings.MAX_THREAD_WORKERS) as executor:
            result = executor.map(
                self.send_one_call_out_email, list(CallOutEmail.get_unsent())
            )

        modified = sum(result)

        stop = time.time()

        self.stdout.write(
            f"Successfully sent {modified} call out emails in {stop - start:.2}s."
        )

    def send_one_call_out_email(self, email: CallOutEmail) -> bool:
        """Send one call out email."""
        sender = mailing_person(settings.MAIN_EMAIL, email.sender)
        to = mailing_persons_from_circonscriptions(email.circonscription_numbers)
        if email.send_to_government:
            to.append(get_gvt_address())
        cc = (mailing_person(email.from_email, email.sender),)

        to = maybe_catchall(to)
        cc = maybe_catchall(cc)

        sending_result = send_mail(
            sender=sender,
            to=to,
            subject=email.subject,
            text=email.content,
            cc=cc,
            instance=email,
        )

        if not sending_result:
            self.stderr.write(f"Sending mail to {email} failed.")
            capture_message(f"Sending mail to {email} failed")

        return sending_result
