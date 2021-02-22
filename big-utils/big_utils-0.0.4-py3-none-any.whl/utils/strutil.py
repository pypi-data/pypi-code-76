"""
A collection of useful string utilities.
"""

# Strings representing boolean *True*
TRUE_STRINGS = ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'ok', 'on', 'ja', 'ya', 'affirmative']

# default value of that's considered 'SHORT'
SHORT_STRING_LEN = 64


def trim(value, default_value=''):
    """
    Removes leading and trailing whitespace from the specified string. If the specified string is composed of
    whitespace only, the specified default value is returned.

    :param value: a string to trim
    :param default_value: a default value to return if the specified string consists of whitespace only.
    :return: a string without any leading or trailing whitespace or the specified default value if
        the specified string consists of whitespace only.
    """
    value = value.strip() if value else None
    return value if value else default_value


def ensure_not_blank(value, message=None):
    """
    Removes leading and trailing whitespace from the specified string and checks whether or not
    it is blank (None or whitespace). If it is, it raises a `ValueError` with the specified `message`.

    :param value: value to check
    :param message: message to pass to ValueError
    :raises ValueError
    """
    message = message if message else "Value must not be blank"
    value = trim(value)
    if value:
        return value
    else:
        raise ValueError(message)


def combine_url(base_url, *args):
    """Combines the base url and the path component, taking care of the slashes"""
    parts = [base_url, *args]
    return '/'.join(s.strip('/') for s in parts)


def string_2_bool(value):
    return trim(value).lower() in TRUE_STRINGS


def truncate_long_text(long_text, max_len=SHORT_STRING_LEN):
    """Reduces an excessively long descriptions to approx. SHORT_STRING_LEN number of characters"""
    long_text = trim(long_text)
    if long_text:
        ellipses = '...'
        adjusted_max_len = max_len + len(ellipses)
        long_text = (long_text[:max_len] + ellipses) if len(long_text) > adjusted_max_len else long_text
    return long_text
