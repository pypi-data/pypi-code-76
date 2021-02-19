""" A Python file to keep all the internal functions that are not meant to be used by the user."""
from RemotePyLib import Exceptions
def validateEmail(email):
    """A function to determine that the email is valid or not.  
    It only checks if the email address contains an @ and a period (.) and the server checks whether or not the email actually exists.

    Args:
        email (str): the email address to be checked
    """
    email = str(email)
    notpresent = []
    if "@" not in email:
        notpresent.append('@')
    if '.'not in email.split('@')[1]:
        notpresent.append('.')
    if len(notpresent) != 0:
        raise Exceptions.InvalidEmailError(email, str(notpresent))
