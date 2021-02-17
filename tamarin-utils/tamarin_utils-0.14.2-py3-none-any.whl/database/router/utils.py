import itertools
import random
import warnings
from functools import wraps
import threading

from django.conf import settings

__all__ = ['this_thread_is_pinned', 'pin_this_thread', 'unpin_this_thread',
           'use_primary_db', 'db_write', 'get_replica', 'PRIMARY_DB_ALIAS']

PRIMARY_DB_ALIAS = getattr(settings, 'TAMARIN_PRIMARY_DB', 'default')

replicas = None

_locals = threading.local()


def this_thread_is_pinned():
    """
    Return whether the current thread should send all its reads to the master DB.
    """
    return getattr(_locals, 'pinned', False)


def pin_this_thread():
    """
    Mark this thread as "stuck" to the master for all DB access.
    """
    _locals.pinned = True


def unpin_this_thread():
    """
    Unmark this thread as "stuck" to the master for all DB access.
    If the thread wasn't marked, do nothing.
    """
    _locals.pinned = False


class UsePrimaryDB(object):
    """
    A contextmanager/decorator to use the master database.
    """

    def __call__(self, function):
        @wraps(function)
        def decorator(*args, **kw):
            with self:
                return function(*args, **kw)

        return decorator

    def __enter__(self):
        _locals.old = this_thread_is_pinned()
        pin_this_thread()

    def __exit__(self, exc_type, exc_value, exc_tb):
        if not _locals.old:
            unpin_this_thread()


use_primary_db = UsePrimaryDB()


def mark_as_write(response):
    """
    Mark a response as having done a DB write.
    """
    response._db_write = True
    return response


def db_write(function):
    @wraps(function)
    def _wrapped(*args, **kw):
        with use_primary_db:
            response = function(*args, **kw)
        return mark_as_write(response)

    return _wrapped


def _get_replica_list():
    global replicas
    if replicas is not None:
        return replicas

    dbs = None
    if hasattr(settings, 'REPLICA_DATABASES'):
        dbs = list(settings.REPLICA_DATABASES)

    if not dbs:
        warnings.warn(
            '[tamarin] No replica databases are configured! '
            'You can configure them with the REPLICA_DATABASES setting.',
            UserWarning,
        )
        replicas = itertools.repeat(PRIMARY_DB_ALIAS)
        return replicas

    # Shuffle the list so the first replica isn't slammed during startup.
    random.shuffle(dbs)

    # Set the replicas as test mirrors of the master.
    for db in dbs:
        settings.DATABASES[db].get('TEST', {})['MIRROR'] = PRIMARY_DB_ALIAS

    replicas = itertools.cycle(dbs)
    return replicas


def get_replica():
    """Returns the alias of a replica database."""
    return next(_get_replica_list())
