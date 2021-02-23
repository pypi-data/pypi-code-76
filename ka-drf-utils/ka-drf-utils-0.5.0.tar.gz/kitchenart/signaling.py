import functools

from django.conf import settings
from django.dispatch import receiver


def custom_receiver(signal, **decorator_kwargs):
    def inner(func):
        @receiver(signal, **decorator_kwargs)
        @functools.wraps(func)
        def wrapper(sender, **kwargs):
            if settings.MUTE_SIGNALS:
                return
            return func(sender, **kwargs)
        return wrapper
    return inner
