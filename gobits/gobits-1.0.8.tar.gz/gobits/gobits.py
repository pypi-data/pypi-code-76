import os
import json

from datetime import datetime
from werkzeug.local import LocalProxy
from json.decoder import JSONDecodeError


class Gobits:
    """
    A small class that gathers information (bits) for a pub/sub message payload.

    Attributes:
        _request                Holds information about the cloud function request.
        _context                Holds information about the cloud function context.
        envelope                The envelope containing a pub/sub message.
        message                 The pub/sub message to be processed.
        processed               Time of processing (UTC).
        gcp_project             The source GCP project.
        execution_id            The id of the execution.
        execution_type          Type of the service processing the message.
        execution_trigger_type  Type of the trigger invoking the processor.
        function_name           Name of the processing cloud function.
        function_version        Version of the processing cloud function.
        event_id                The id of the trigger event.
        message_id              The pub/sub message id.
        message_publish_time    Time of publishing to pub/sub (UTC).
        source_subscription     The originating pub/sub subscription.
    """

    def __init__(self, request: LocalProxy = None, context=None):
        self._request = request
        self._context = context

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        self._request = value

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    @property
    def envelope(self):
        if self._request:
            try:
                return json.loads(self._request.data.decode('utf-8'))
            except JSONDecodeError:
                return {}
        else:
            return {}

    @property
    def message(self):
        return self.envelope.get('message', {})

    @property
    def processed(self):
        return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    @property
    def gcp_project(self):
        return os.getenv('X_GOOGLE_GCP_PROJECT')

    @property
    def execution_id(self):
        if self._request:
            return self._request.headers.get('Function-Execution-Id')
        return None

    @property
    def execution_type(self):
        if os.getenv('X_GOOGLE_FUNCTION_NAME'):
            return 'cloud_function'

        if os.getenv('BUILDER_OUTPUT'):
            return 'cloud_build'

        if os.getenv('GAE_APPLICATION'):
            return 'google_app_engine'

        return None

    @property
    def execution_trigger_type(self):
        return os.getenv('FUNCTION_TRIGGER_TYPE')

    @property
    def function_name(self):
        return os.getenv('X_GOOGLE_FUNCTION_NAME')

    @property
    def function_version(self):
        return os.getenv('X_GOOGLE_FUNCTION_VERSION')

    @property
    def event_id(self):
        if self._context:
            return self._context.event_id
        return None

    @property
    def message_id(self):
        return self.message.get('messageId')

    @property
    def message_publish_time(self):
        return self.message.get('publishTime')

    @property
    def source_subscription(self):
        return self.envelope.get('subscription')

    @classmethod
    def from_request(cls, request):
        return cls(request=request)

    @classmethod
    def from_context(cls, context):
        return cls(context=context)

    def to_json(self):

        gobits = {
            'processed': self.processed,
            'gcp_project': self.gcp_project,
            'execution_id': self.execution_id,
            'execution_type': self.execution_type,
            'execution_trigger_type': self.execution_trigger_type,
            'function_name': self.function_name,
            'function_version': self.function_version,
            'event_id': self.event_id,
            'message_id': self.message_id,
            'message_publish_time': self.message_publish_time,
            'source_subscription': self.source_subscription
        }

        response = {k: v for (k, v) in gobits.items() if v}

        return response
