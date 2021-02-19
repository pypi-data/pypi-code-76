from decimal import Decimal

from django.contrib.humanize.templatetags.humanize import intcomma


def humanize_amount(amount_value):
    """
    This function is used to format the provided amount value into a human readable format.

    :param amount_value: float: Amount value to be formatted
    :return: str: Comma separated amount value
    """
    if amount_value:
        return intcomma(amount_value)
    return 0


def to_decimal(x):
    """
    This function is used to convert a numeric value into a decimal value.

    :param x:
    :return: Decimal:
    """
    if not x:
        x = 0
    return Decimal(x)


def to_int(x):
    """
    This function is used to convert a numeric value into an int value.

    :param x:
    :return: int:
    """
    if not x:
        x = 0
    return int(x)


def is_greater(a, b):
    """
    This function takes in two numeric values and compares if one is greater than the other.

    :param a:
    :param b:
    :return: bool: Returns True or False
    """
    return to_decimal(a) > to_decimal(b)


def is_less(a, b):
    """
    This function takes in two numeric values and compares if one is less than the other.

    :param a:
    :param b:
    :return: bool: Returns True or False
    """
    return to_decimal(a) < to_decimal(b)


def is_equal(a, b):
    """
    This function takes in two numeric values and compares if the two values are equal.

    :param a:
    :param b:
    :return: bool: Returns True or False
    """
    return to_decimal(a) == to_decimal(b)


def is_greater_or_equal(a, b):
    """
    This function takes in two numeric values and compares if one is greater or equal to the other.

    :param a:
    :param b:
    :return: bool: Returns True or False
    """
    return to_decimal(a) >= to_decimal(b)


def add(a, b):
    """
    This function takes in two numeric values and returns a sum of those two numbers.

    :param a:
    :param b:
    :return: Decimal:
    """
    return to_decimal(a) + to_decimal(b)


def multiply(a, b):
    """
    This function takes in two numeric values and multiplies the two numbers.

    :param a:
    :param b:
    :return: Decimal:
    """
    return to_decimal(a) * to_decimal(b)


def divide(a, b):
    """
    This function takes in two numeric values and divides the two numbers.

    :param a:
    :param b:
    :return: Decimal:
    """
    return to_decimal(a) / to_decimal(b)


def subtract(a, b):
    """
    This function takes in two numeric values and subtracts one from the other.

    :param a:
    :param b:
    :return: Decimal:
    """
    return to_decimal(a) - to_decimal(b)
