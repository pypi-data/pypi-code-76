"""
    Common Utilitie functions.
"""
import sys


def tabulate(data):
    """Make dict or list to table ready tuples."""
    if isinstance(data, dict) and data:
        headers = data.keys()
        rows = [value for key, value in data.items()]
    elif isinstance(data, list) and data:
        headers = data[0].keys()
        rows = [[value for key, value in obj.items()] for obj in data]
    else:
        return (), ()

    return headers, rows


def is_tty():
    return sys.stdin.isatty()


def yes_or_no(confirmation_message, default_yes=False):
    if default_yes:
        options = "[Y/n]"
    else:
        options = "[y/N]"
    user_response = input(confirmation_message + options).lower()
    if user_response not in ('y', 'n'):
        return default_yes
    return user_response == 'y'
