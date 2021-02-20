import time
from argparse import ArgumentParser

from . import BaseCommand

from appel_crises.models import Signature

FAKE_ATTRIBUTES = dict(first_name="PURE", surname="Spammer", news=False)


def generate_a_fake_signature(n: int) -> Signature:
    """Generate a fake signature based on integer n."""
    return Signature(email=f"spammer+f{n}f@dev.p-u-r-e.tech", **FAKE_ATTRIBUTES)


class Command(BaseCommand):
    help = (
        "Populate the database with fakes signatures or remove them from the database. "
    )

    def add(self, n: int):
        self.remove()
        signatures = (generate_a_fake_signature(i) for i in range(n))
        inserted = len(Signature.objects.bulk_create(signatures))

        return inserted

    def remove(self) -> int:
        removed, _ = Signature.objects.filter(**FAKE_ATTRIBUTES).delete()

        return removed

    def add_arguments(self, parser: ArgumentParser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "-a", "--add", type=int, help="Add ADD entries to the database"
        )
        group.add_argument("-r", "--remove", action="store_true")

    def handle(self, *args, **options):
        if options['remove']:
            start = time.time()
            removed = self.remove()
            stop = time.time()
            self.stdout.write(
                f"Removed {removed} objects from the database in {stop - start:.2}s."
            )
        elif 'add' in options:
            start = time.time()
            inserted = self.add(options['add'])
            stop = time.time()
            self.stdout.write(
                f"Added {inserted} signatures into the databasein {stop - start:.2}s.\n"
                f"They looked like this :\n Signature"
                f"[{', '.join(k + '=' + str(v) for k, v in FAKE_ATTRIBUTES.items())}]\n"
            )
