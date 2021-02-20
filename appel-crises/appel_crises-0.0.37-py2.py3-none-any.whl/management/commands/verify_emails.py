import time
from typing import List

from . import BaseCommand

from appel_crises.mailer import get_delivered_emails, DeliveryResult
from appel_crises.models import EmailOffset, Signature


class Command(BaseCommand):
    help = "Fetch all the delivered emails and mark them as verified"

    def handle(self, *args, **kwargs):
        """Do the job."""
        start = time.time()
        limit = 100
        offset = EmailOffset.get_max_offset()
        last_fetched = limit
        counter = 0

        # While there may be emails to mark as verified, do:
        while last_fetched == limit:

            # because @async_to_sync does not fix correctly typechecking
            # noinspection PyTypeChecker
            results: List[DeliveryResult] = get_delivered_emails(offset, limit)

            offset += len(results)
            last_fetched = len(results)

            for (email, date) in results:
                if Signature.mark_email_as_verified(email, date):
                    counter += 1
                else:
                    self.stderr.write(f"Email not in the database: {email}")
                    # Too much events for sentry ...
                    # capture_message(f"Email not in the database: {email}")

        EmailOffset(offset=offset).save()
        stop = time.time()
        self.stdout.write(f"Total: verified {counter} emails in {stop - start:.2}s.")
