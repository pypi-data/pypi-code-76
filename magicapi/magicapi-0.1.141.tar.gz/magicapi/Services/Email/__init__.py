from typing import List
import smtplib
import ssl

from magicapi import g


port, smtp_server = g.settings.email_port, g.settings.email_smtp_server
sender_email, sender_password = g.settings.sender_email, g.settings.sender_password
from magicapi.Decorators.background_tasks import run_in_background


def send_email(text: str, recipients: List[str], subject: str = None):
    if subject:
        text = f"Subject: {subject}\n\n{text}"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_password)
        for recipient in recipients:
            server.sendmail(sender_email, recipient, text)


@run_in_background
def send_email_in_background(text: str, recipients: List[str], subject: str = None):
    send_email(text=text, recipients=recipients, subject=subject)


if __name__ == "__main__":
    send_email(
        subject="what do you know about Mactard Jones?",
        text="nothing, I hope",
        recipients=["fernando@basement.social"],
        # recipients=["kellycup8@gmail.com"],
    )
