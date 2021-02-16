from functools import wraps

# from magicapi import settings
from magicapi import g
from magicapi.Errors import BackendException

from magicapi.Services.Doorman import CurrentUser

from magicapi.Services import Segment

from magicapi.Decorators.helpers import async_safe


def segment(keywords=None):
    def inner_function(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            if not g.settings.segment_write_key:
                raise BackendException(
                    message="You cannot use the segment decorator without the SEGMENT_WRITE_KEY env variable."
                )
            for key, val in kwargs.items():
                if issubclass(val.__class__, CurrentUser):
                    uid = val.uid
                    action = f.__name__
                    segment_d = {}
                    if keywords:
                        segment_d = {k: kwargs.get(k) for k in keywords}
                    Segment.track(uid, action, segment_d)
            return await async_safe(f, *args, **kwargs)

        return wrapper

    return inner_function
