from ..command import Command
from .utils.functions import config_scope, Level, validate_status
from sentry_sdk import capture_event


class SentryCommand(Command):
    def __init__(self, response, status_code):
        super(SentryCommand, self).__init__()
        self._response = response
        self._status_code = status_code

    def execute(self):
        response = self._response
        status = response.get('status')
        metadata = response.get('metadata')
        status_code = self._status_code
        if validate_status(status_code):
            if status == 'failed':
                config_scope(metadata, status_code, Level.ERROR)
                sentry_exception_code = capture_event({
                    'error': response.get('error')
                })
            elif status == 'success':
                config_scope(metadata, status_code, Level.INFO)
                sentry_exception_code = capture_event(
                    {
                        'data': response.get('data'),
                        'message': 'request was successfully submitted'
                    }
                )
            else:
                config_scope(metadata, status_code, Level.ERROR)
                sentry_exception_code = capture_event(
                    {
                        'response': response,
                        'message': F'status is invalid ({status})'
                    }
                )
            return {'sentry_code': sentry_exception_code}
        else:
            return {}
