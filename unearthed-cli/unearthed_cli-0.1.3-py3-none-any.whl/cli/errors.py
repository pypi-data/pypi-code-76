from sys import exit
from traceback import print_exc  # print_tb
from uuid import uuid4

import click
from colorama import Back, Fore, Style


def bail(e, text):
    error_filename = "error-" + str(uuid4())[:8] + ".txt"
    with open(error_filename, "w") as tmp:
        print_exc(file=tmp)
    error_text = getattr(e, "explanation", str(e))
    message = "\n" + Fore.RED + u"\u2718" + " "
    message += text + "\n\n"
    message += Style.RESET_ALL
    message += "The full error has been stored in a file called {} {} {}\n".format(
        Fore.GREEN, error_filename, Style.RESET_ALL
    )
    message += "which you can email to {}{}{} for support.\n".format(
        Fore.GREEN, "dev@unearthed.solutions", Style.RESET_ALL
    )
    message += "{}Error: {}{}\n".format(Fore.RED, error_text, Style.RESET_ALL)
    exit(message)


def check_latest_version():
    try:
        from outdated import check_outdated
        from pkg_resources import get_distribution

        dist = get_distribution("unearthed-cli")
        return check_outdated("unearthed-cli", dist.version)
    except Exception:
        return [None, None]


def check_version_and_warn():
    is_outdated, latest_version = check_latest_version()
    if is_outdated:
        message = Fore.YELLOW
        message += "There is a newer version of the unearthed command available.\n"
        message += "Please install it like this: pip install --upgrade unearthed\n"
        message += Style.RESET_ALL
        click.echo(message)
