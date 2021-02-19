from enum import IntEnum
import logging
import logging.config
import os

import click
from google.cloud import logging_v2

ENABLE_CLOUD_LOGGING = 'ENABLE_CLOUD_LOGGING'


class CloudLoggingSeverity(IntEnum):
    NOTSET = 0
    DEBUG = 100
    INFO = 200
    WARNING = 400
    ERROR = 500
    CRITICAL = 600


class CloudLoggingHandler(logging.Handler):
    """Logs to Google Cloud Logging."""

    def __init__(self, level=logging.DEBUG, name='rbx'):
        super().__init__(level=level)
        if self.cloud_logging_enabled:
            self.writer = CloudLoggingWriter(name=name)

    @property
    def cloud_logging_enabled(self):
        return bool(os.getenv(ENABLE_CLOUD_LOGGING, False))

    def emit(self, record):
        if self.cloud_logging_enabled:
            if record.exc_info:
                message = logging.Formatter().formatException(record.exc_info)
            else:
                message = self.format(record)

            self.writer.write_entry(message, severity=CloudLoggingSeverity[record.levelname])


class CloudLoggingWriter:
    """The Writer is the object that calls the Cloud Logging API."""

    def __init__(self, name):
        self.client = logging_v2.LoggingServiceV2Client()
        self.name = name
        self.project = os.environ['GOOGLE_CLOUD_PROJECT']
        self.resource = {
            'type': 'gae_app',
            'labels': {
                'project_id': self.project,
                'module_id': os.environ['GAE_SERVICE'],
                'version_id': os.environ['GAE_VERSION'],
            }
        }

    def write_entry(self, message, severity=CloudLoggingSeverity.NOTSET):
        entry = logging_v2.types.LogEntry(text_payload=message, severity=severity)
        self.client.write_log_entries(
            [entry],
            log_name=f'projects/{self.project}/logs/{self.name}',
            resource=self.resource)


class ColourFormatter(logging.Formatter):

    def format(self, record):
        message = super().format(record)
        colours = {
            logging.INFO: {'bold': True},
            logging.WARNING: {'fg': 'yellow'},
            logging.ERROR: {'fg': 'bright_red'},
            logging.CRITICAL: {'fg': 'bright_white', 'bg': 'red'},
        }
        try:
            message = click.style(message, **colours[record.levelno])
        except KeyError:
            pass
        return message
