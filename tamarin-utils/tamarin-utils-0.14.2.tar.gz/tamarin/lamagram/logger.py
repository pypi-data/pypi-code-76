from logging import StreamHandler, critical
from django.conf import settings
from logging import LogRecord
import requests


class LamagramHandler(StreamHandler):

    def __init__(self, url=None, token=None):
        super(LamagramHandler, self).__init__()

    def emit(self, record: LogRecord):
        message = self.format(record)
        try:
            requests.post(
                getattr(settings, 'TITI_URL', ''),
                json=message,
                headers={
                    "Authorization": getattr(settings, 'TITI_TOKEN', '')
                }
            )
        except requests.ConnectionError:
            critical('connect to titi failed')
        except Exception:
            critical('error has been occured (send bonobo-exception)')

    def format(self, record: LogRecord):
        message = F"{record.name} `{record.module}` \n" \
                  F"`{record.pathname}` {record.lineno} \n" \
                  F"`{record.getMessage()}`"
        return {
            'message': message,
            'code': 'bonobo-exception',
        }
