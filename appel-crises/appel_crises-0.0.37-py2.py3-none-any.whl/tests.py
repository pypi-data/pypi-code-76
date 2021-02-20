from django import test

from . import mailer
from .management.commands import send_emails


class HelperTests(test.TestCase):

    INPUTS = [
        mailer.mailing_person(email='john@doe.com', name="John Doe"),
        mailer.mailing_person(email='jane@doe.org'),
    ]

    @test.override_settings(MAILING_CATCHALL='')
    def test_catchall_unset(self):
        out = send_emails.maybe_catchall(self.INPUTS)
        self.assertEqual(out, self.INPUTS)

    @test.override_settings(MAILING_CATCHALL='root+{}@example.org')
    def test_catchall_set(self):
        out = send_emails.maybe_catchall(self.INPUTS)
        self.assertEqual(
            [
                mailer.mailing_person(
                    email='root+john_at_doe.com@example.org', name="John Doe",
                ),
                mailer.mailing_person(email='root+jane_at_doe.org@example.org'),
            ],
            out,
        )
