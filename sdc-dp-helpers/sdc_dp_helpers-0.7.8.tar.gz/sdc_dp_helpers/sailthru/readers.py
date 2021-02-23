"""
    CUSTOM READERS CLASSES
        - Class which manages reader tasks like auth, requests, pagination
"""
import os
from contextlib import contextmanager
from datetime import datetime, timedelta

import yaml
from sailthru import SailthruClient

from sdc_dp_helpers.api_utilities.retry_managers import request_handler


class CustomSailThruReader:
    """
        Custom SailThru Reader
    """

    def __init__(self, api_key_path):
        self.api_key_path = api_key_path
        self.sailthru_client = SailthruClient(
            api_key=self.get_api_key()[0],
            secret=self.get_api_key()[1]
        )

    def get_api_key(self) -> list:
        """
            Gathers key and value pairs of key and their secret.
        """
        with open(self.api_key_path, 'r') as file:
            data = yaml.safe_load(file)
            return [data.get('api_key'), data.get('api_secret')]

    @request_handler(
        wait=int(os.environ.get('REQUEST_WAIT_TIME', 0.1)),
        backoff_factor=float(os.environ.get('REQUEST_BACKOFF_FACTOR', 0.01)),
        backoff_method=os.environ.get('REQUEST_BACKOFF_METHOD', 'random')
    )
    @contextmanager
    def call_api_context(self, query_config, filter_now=True):
        """
            Makes use of the SaliThru client, constructs a query,
            and returns the data.
            :query_config: dict. A specific config file that constructs
                           the api Query.
            :filter_now: bool. Flag to set date filter to dynamic,
                         in this case yesterdays data.
            :return: list. Returns a dict, first one is the metadata
                     and the second is the data itself.

            To use the context use 'with', expect none when no more data is
            available in the context request session:

            data_set = []
            with reader.call_api_context(query_config='query_config.yml') as query:
                data_set.append(query)
        """

        now = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

        with open(query_config, 'r') as file:
            query = yaml.safe_load(file)

        query_config = query.get('query_config')
        print('Query config:{}'.format(query_config))

        # can handle multiple metrics, or just one
        for query in query_config:
            try:
                # dynamically add date range if filter_now is true
                if filter_now:
                    query['data'].update({
                        'start_date': now, 'end_date': now
                    })
                elif (query['data'].get('start_date', None) is None
                      or query['data'].get('end_date', None) is None):
                    raise ValueError('The start_date and end_date is required,'
                                     'or set filter_now to true.')

                response = self.sailthru_client.api_get(
                    action=query.get('action'),
                    data=query.get('data')
                )

                if not response.is_ok():
                    error = response.get_error()
                    raise RuntimeError('APIError: {}, Status Code: {}, Error Code: {}'.format(
                        error.get_message(),
                        str(response.get_status_code()),
                        str(error.get_error_code()))
                    )

                # append metadata to query result
                response_data = response.get_body()
                response_data['action'] = query.get('action')
                response_data['stat'] = query.get('data').get('stat')
                response_data['template'] = query.get('data').get('template')

                yield response_data

            except Exception as err:
                raise err
