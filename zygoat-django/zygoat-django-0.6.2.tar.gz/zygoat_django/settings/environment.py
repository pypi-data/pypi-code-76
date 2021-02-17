"""
Environment variable configuration for zygoat projects. We utilize `django-environ`_ to make using environment variables painless and easy, and configure the ``DEBUG`` and ``PRODUCTION`` values to distinguish your environments.

This module exposes a few utilities:

.. autodata:: env
"""

import environ

env = environ.Env()

PRODUCTION = env.bool("DJANGO_PRODUCTION", default=False)
"""
:annotation: = False

Whether or not the app is running production mode.

If ``True``, ``DEBUG`` is explicitly set to ``False`` to avoid leaking information.

.. note::
   Controlled by the environment variable ``DJANGO_PRODUCTION`` by default
"""

DEBUG = False if PRODUCTION else env.bool("DJANGO_DEBUG", default=True)
"""
:annotation: = True

Used internally by Django to decide how much debugging context is sent to the browser when a failure occurs.

Cannot be ``True`` if ``PRODUCTION`` is ``True``

.. note::
   Controlled by the environment variable ``DJANGO_DEBUG`` by default
"""


def prod_required_env(key, default, method="str"):
    """
    Throw an exception if PRODUCTION is true and the environment key is not provided

    :type key: str
    :param key: Name of the environment variable to fetch
    :type default: any
    :param default: Default value for non-prod environments
    :type method: str
    :param method: django-environ instance method, used to type resulting data

    .. seealso::
       - `django-environ <https://github.com/joke2k/django-environ>`_
       - `django-environ supported types <https://github.com/joke2k/django-environ#supported-types>`_
    """
    if PRODUCTION:
        default = environ.Env.NOTSET
    return getattr(env, method)(key, default)


ALLOWED_HOSTS = [prod_required_env("DJANGO_ALLOWED_HOST", default="*")]
"""
:annotation: = ['*']

Sets the list of valid ``HOST`` header values. Typically this is handled by a reverse proxy in front of the deploy Django application. In development, this is provided by the Caddy reverse proxy.

.. warning:: Requires ``DJANGO_ALLOWED_HOST`` to be set in production mode
"""

db_config = env.db_url("DATABASE_URL", default="postgres://postgres:postgres@db/postgres")
"""
:annotation: = env.db_url("DATABASE_URL", default="postgres://postgres:postgres@db/postgres")

Parses the ``DATABASE_URL`` environment variable into a Django `databases`_ dictionary.

Uses a standard database URI schema.
"""

DATABASES = {"default": db_config}
"""
Django `databases <https://docs.djangoproject.com/en/3.1/ref/settings/#databases>`_ configuration value.

The default entry is generated automatically from :py:data:`db_config`.

.. note::
   If you need more than one database or a different default setup, you can modify this value in your application's ``settings.py`` file.
"""
