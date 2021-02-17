from django.conf import settings
from tamarin import status

SENTRY_ALLOWED_ALL = getattr(settings, 'SENTRY_ALLOWED_ALL', False)
SENTRY_ALLOWED_STATUS = getattr(settings, 'SENTRY_ALLOWED_STATUS', [])


def validate_status(status_code):
    if SENTRY_ALLOWED_ALL:
        return True
    allowed_condition = [getattr(status, F'is_{method}', None) for method in SENTRY_ALLOWED_STATUS]
    for condition in allowed_condition:
        if condition and condition(status_code):
            return True
    if status_code in SENTRY_ALLOWED_STATUS:
        return True
    return False
