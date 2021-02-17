"""
Cache configuration for zygoat projects. We use ``django-redis`` to handle connecting to the cache backend, and then tell django to use a write-through cache backend for sessions. This makes sessions blazingly fast and persistent in the case that the cache gets cleared.
"""

from .environment import prod_required_env

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": prod_required_env("DJANGO_REDIS_CACHE_URL", "redis://cache:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
"""
Configures the default cache to point to the zygoat generated docker container.
"""

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
"""
.. seealso::
   - `How to use sessions <https://docs.djangoproject.com/en/3.1/topics/http/sessions/>`_
   - `Using cached sessions <https://docs.djangoproject.com/en/3.1/topics/http/sessions/#using-cached-sessions>`_
"""
