import sentry_sdk
from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration


def init():
    url = getattr(settings, 'SENTRY_URL', None)
    key = getattr(settings, 'SENTRY_KEY', None)
    organization = getattr(settings, 'SENTRY_ORGANIZATION', None)
    project = getattr(settings, 'SENTRY_PROJECT', None)
    if url:
        sentry_sdk.init(
            dsn=url,
            integrations=[DjangoIntegration(), CeleryIntegration()],
            send_default_pii=True
        )
    elif key and organization and project:
        sentry_sdk.init(
            dsn=F"https://{key}@{organization}.ingest.sentry.io/{project}",
            integrations=[DjangoIntegration(), CeleryIntegration()],
            send_default_pii=True
        )
    else:
        raise Exception('sentry config is not provided')
