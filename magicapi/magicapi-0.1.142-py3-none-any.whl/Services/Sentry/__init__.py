import sentry_sdk
from sentry_sdk import capture_exception
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from magicapi import g

from magicapi.Decorators.background_tasks import run_in_background

HAS_SENTRY_DSN = g.settings.sentry_dsn
if HAS_SENTRY_DSN:
    sentry_sdk.init(
        dsn=g.settings.sentry_dsn,
        traces_sample_rate=g.settings.sentry_traces_sample_rate,
        send_default_pii=True,
        request_bodies="always",
    )
