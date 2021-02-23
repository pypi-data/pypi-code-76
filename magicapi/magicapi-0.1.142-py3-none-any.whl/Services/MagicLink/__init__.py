from typing import Callable
from magicdb import auth
from magicapi.Services.MagicLink.template import make_template_and_subject


def make_magic_link(email_address: str, redirect_url: str):
    action_code_settings = auth.ActionCodeSettings(url=redirect_url)
    magic_link = auth.generate_sign_in_with_email_link(
        email_address, action_code_settings
    )
    return magic_link


def get_magic_link_template_and_subject(email_address: str, redirect_url: str):
    magic_link = make_magic_link(email_address=email_address, redirect_url=redirect_url)
    magic_template, subject = make_template_and_subject(
        email_address=email_address, magic_link=magic_link
    )
    return magic_template, subject


def send_magic_link_email(
    sender_function: Callable, email_address: str, redirect_url: str
):
    """The sender function must take in a text, subject, and recipients"""
    magic_template, subject = get_magic_link_template_and_subject(
        email_address=email_address, redirect_url=redirect_url
    )
    return sender_function(
        text=magic_template, subject=subject, recipients=[email_address]
    )


if __name__ == "__main__":
    magic_template, subject = make_template_and_subject(
        email_address="kellycup8@gmail.com", magic_link="www.penguincbd.com"
    )
    print(magic_template, subject)
