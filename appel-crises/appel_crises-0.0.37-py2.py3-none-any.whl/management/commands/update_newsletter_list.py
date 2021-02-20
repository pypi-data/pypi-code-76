import time

from . import BaseCommand

from appel_crises.mailer import add_signatures_to_newsletter_list
from appel_crises.models import Signature


class Command(BaseCommand):
    help = "Add emails from signatures to the SendInBlue list"

    def handle(self, *args, **kwargs):
        """Do the job."""
        start = time.time()

        signatures = Signature.get_validated().filter(
            added_to_newsletter_list=False, news=True
        )

        add_signatures_to_newsletter_list(signatures)

        modified = signatures.update(added_to_newsletter_list=True)

        self.stdout.write(
            "lauched SIB process to import {} contacts in {:.2f}s".format(
                modified, time.time() - start
            )
        )
