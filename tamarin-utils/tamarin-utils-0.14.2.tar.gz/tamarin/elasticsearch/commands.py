from tamarin.elasticsearch.client import ElasticSearchClient
from .config import CURRENT_TIME_ZONE, ALLOWED_STATUS
from tamarin.elasticsearch.utils.functions import validate_status, var2str
from tamarin.command import Command
from sentry_sdk import capture_exception
import uuid
import datetime
from tamarin.logs.models import Report
import traceback


class ElasticSearchCommand(Command):
    def __init__(self, response, status_code, index, doc, args=None, params=None, headers=None):
        super(ElasticSearchCommand, self).__init__()
        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if args is None:
            args = {}
        self._response = response
        self._status_code = status_code
        self._index = index
        self._doc = doc
        self._args = args
        self._params = params
        self._headers = headers

    def execute(self):
        try:
            response = self._response
            index = self._index
            if validate_status(self._status_code):
                metadata = response.get('metadata')
                transaction = metadata.pop('transaction', {})
                created_at = datetime.datetime.now(tz=CURRENT_TIME_ZONE)
                doc = self._doc
                params = self._params
                headers = self._headers
                client = ElasticSearchClient.get_client()
                elastic_id = metadata.get('id', F"{uuid.uuid4()}-{created_at.timestamp()}")
                body = {
                    'status': response.get('status'),
                    'metadata': metadata,
                    'transaction': self.clean_data_type(transaction),
                    'created_at': created_at,
                }
                if response.get('data'):
                    body.update({
                        'data': self.clean_data_type(response.get('data')),
                    })
                if response.get('error'):
                    error = response.get('error')
                    error = {
                        'messages': self.clean_data_type(error.get('message')),
                        'code': error.get('code')
                    }
                    body.update({'error': error})
                body = var2str(body)
                client.index(
                    index=index,
                    body=body,
                    doc_type=doc,
                    id=elastic_id,
                    params=params,
                    headers=headers
                )
                return {'elastic_id': elastic_id}
            else:
                return {'elastic_id': 'not allowed'}
        except Exception as e:
            capture_exception(e)
            report = Report.objects.create(
                index='elastic-exception',
                status=500,
                text=traceback.format_exc()
            )
            return {
                'elastic_id': 'exception occured',
                'report': report.id,
            }

    def clean_data_type(self, data):
        if data is None:
            return []
        if type(data) == list:
            return data
        else:
            return [data]
