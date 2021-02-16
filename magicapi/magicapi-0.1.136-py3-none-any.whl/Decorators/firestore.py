import os
from functools import wraps
from magicapi.Errors import FirestoreException

from magicapi.Decorators.helpers import async_safe


def need_firestore(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            raise FirestoreException(
                message="You must supply a firestore service account to use this endpoint!"
            )
        return await async_safe(f, *args, **kwargs)

    return wrapper
