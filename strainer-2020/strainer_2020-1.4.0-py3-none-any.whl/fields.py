from . import validators
from .formatters import format_datetime
from .structure import field


def _date_time_field(
            typename, source_field, target_field=None, attr_getter=None, required=False
        ):
    type_validators = {
        'date': validators.date,
        'time': validators.time,
        'datetime': validators.datetime,
    }
    field_validators = [type_validators[typename]()]
    if required:
        field_validators.insert(0, validators.required())
    formatters = [format_datetime()]
    return field(
        source_field, target_field=target_field, attr_getter=attr_getter,
        validators=field_validators, formatters=formatters,
    )


def date(source_field, target_field=None, attr_getter=None, required=False):
    return _date_time_field('date', source_field, target_field, attr_getter, required)


def datetime(source_field, target_field=None, attr_getter=None, required=False):
    return _date_time_field(
        'datetime', source_field, target_field, attr_getter, required
    )


def time(source_field, target_field=None, attr_getter=None, required=False):
    return _date_time_field('time', source_field, target_field, attr_getter, required)
