from functools import partial, wraps

import aniso8601

from .exceptions import ValidationException


def export_validator(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        return partial(f, *args, **kwargs)

    return wrapper


def clamp_to_interval(value, bounds):
    min_bound, max_bound = bounds
    return min(max_bound, max(min_bound, value))


@export_validator
def integer(value, bounds=None, context=None):
    """Converts a value to integer, applying optional bounds."""
    try:
        value = int(value)
        if bounds:
            return clamp_to_interval(value, bounds)
        return value
    except (TypeError, ValueError):
        raise ValidationException('This field is not an integer')


@export_validator
def string(value, max_length=None, context=None):
    """Converts a value into a string, optionally with a max length"""
    if not value:
        return value

    try:
        value = str(value)
    except (TypeError, ValueError):
        raise ValidationException('This field isn\'t a string')

    if max_length and len(value) > max_length:
        raise ValidationException(f'This field is to long, max length is {max_length}')

    return value


@export_validator
def required(value, context=None):
    """validates that a field exists in the input"""
    if value:
        return value

    if value == 0:
        return value

    raise ValidationException('This field is required')


@export_validator
def boolean(value, context=None):
    """Converts a field into a boolean"""
    try:
        return bool(value)
    except (TypeError, ValueError):
        raise ValidationException('This field is supposed to be boolean')


def _date_time_validator(value, typename, context=None):
    parse_funcs = {
        'date': aniso8601.parse_date,
        'time': aniso8601.parse_time,
        'datetime': aniso8601.parse_datetime,
    }
    if not value:
        return
    try:
        return parse_funcs[typename](value)
    except ValueError:
        raise ValidationException(f'Invalid {typename}: {value}')


@export_validator
def datetime(value, context=None):
    """Validates that a a field is an ISO 8601 string, and converts it to a
    datetime object."""
    return _date_time_validator(value, 'datetime', context)


@export_validator
def date(value, context=None):
    """Validates that a a field is an ISO 8601 string, and converts it to a
    date object."""
    return _date_time_validator(value, 'date', context)


@export_validator
def time(value, context=None):
    """Validates that a a field is an ISO 8601 string, and converts it to a
    time object."""
    return _date_time_validator(value, 'time', context)
