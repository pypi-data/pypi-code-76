from django.core import management
import sentry_sdk


class BaseCommand(management.BaseCommand):
    def execute(self, *args, **kwargs):
        try:
            super().execute(*args, **kwargs)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise
