from functools import partial, wraps


def export_formatter(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        return partial(f, *args, **kwargs)

    return wrapper


@export_formatter
def format_datetime(value, context=None):
    """Formats a value as an iso8601 date/time.

    Formatting preserves timezone information if present.
    """
    if not value:
        return value
    return value.isoformat()
