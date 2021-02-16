"""App configuration for django-iconify."""
from django.conf import settings

_prefix = "ICONIFY_"

JSON_ROOT = getattr(settings, f"{_prefix}JSON_ROOT")
