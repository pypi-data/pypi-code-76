import logging
import time
from collections import UserList
from datetime import date
from random import random
from typing import Callable, List

from apiclient.errors import HttpError

from api_connectors.integrations.google_base import GoogleBase


class GoogleListResponse(UserList):
    """ Default wrapper for  """

    def __init__(self, api_response: dict):
        super().__init__(initlist=api_response.pop('items'))

        self.kind = api_response.pop('kind', None)
        self.username = api_response.pop('username', None)
        self.total_results = api_response.pop('totalResults', None)
        self.start_index = api_response.pop('startIndex', None)
        self.items_per_page = api_response.pop('itemsPerPage', None)

        self.others = api_response


class GoogleAnalyticsAPI_V4(GoogleBase):
    """ Google Analytics API is a proxy sub-library for an origin Python API library of Google.
        So it is rather different from other APIs.

        :arg credentials:

        For now, here supports only Core API v3
        Documentation: https://developers.google.com/analytics/devguides/reporting/core/v3?hl=ru
    """
    resource_name = 'analyticsreporting'
    version = 'v4'

    def request_processing(self, call_request: Callable):
        """ Performs handling the 500 errors """
        tries = 0
        while tries < 5:
            tries += 1
            try:
                return call_request(num_retries=1)
            except HttpError as err:
                # Да, я тоже ахуел, но это кусок из офф.доки:
                #   https://developers.google.com/analytics/devguides/reporting/core/v3/errors?hl=ru
                sleep_time = (3 ** tries) + random() * 7
                logging.warning(f'Troubles in the hole.\n'
                                f'Error: {err}, reason: {err.resp.reason}, text: {err.content}.\n'
                                f'Variables:\nn: {tries}; sleep: {sleep_time}')
                if int(err.resp.status_code) >= 500:
                    time.sleep(sleep_time)
                else:
                    raise err

        raise Exception("Couldn't execute the request")

    def get_report(self,
                   profile_id: str,
                   metrics: List[str],
                   dimensions: List[str],
                   start_date: date,
                   end_date: date,
                   filters: List[dict],
                   max_results=10_000,
                   batch_limit=0):
        """ Realize method `batchGet` of `reports`.
            Documentation:  https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet
        """
        params = {
            'reportRequests': [
                {
                    'viewId': f'ga:{profile_id}',
                    'dateRanges': [
                        {
                            'startDate': start_date.strftime('%Y-%m-%d'),
                            'endDate': end_date.strftime('%Y-%m-%d')
                        }],
                    'metrics': [{'expression': metr} for metr in metrics],
                    'dimensions': [{'name': dim} for dim in dimensions],
                    'samplingLevel': 'LARGE',
                    'pageSize': max_results,
                    'metricFilterClauses': [{
                        'filters': [{
                            'metricName': f_r['metric'],
                            'operator': f_r['op'],
                            'comparisonValue': f_r['value']
                        } for f_r in filters]
                    }]

                }
            ]
        }

        first_response = self.request_processing(
            self.client.reports().batchGet(body=params).execute
        )['reports'][0]
        total_results = int(first_response['data']['totals'][0]['values'][0])

        yield_handler = lambda x: [
            *x['dimensions'],
            *[z for y in x['metrics']
              for z in y['values']]
        ]
        yield from map(yield_handler, first_response['data'].get('rows', []))

        batch_limit -= 1
        if total_results > max_results:
            params['reportRequests'][0]['pageToken'] = first_response['nextPageToken']
            while batch_limit != 0:
                response = self.request_processing(
                    self.client.reports().batchGet(body=params).execute
                )['reports'][0]

                yield from map(yield_handler, response['data'].get('rows', []))
                batch_limit -= 1

                if 'nextPageToken' not in response:
                    break

                start_index = int(response['nextPageToken'])
                cur_index = max_results + start_index
                if total_results > cur_index and batch_limit != start_index // max_results:
                    params['reportRequests'][0]['pageToken'] = response['nextPageToken']
                else:
                    break


class GoogleAnalyticsAPI_V3(GoogleBase):
    """ Google Analytics API is a proxy sub-library for an origin Python API library of Google.
        So it is rather different from other APIs.

        :arg credentials: a dictionary with data is needed for GA connection

        For now, here supports only Core API v3
        Documentation: https://developers.google.com/analytics/devguides/reporting/core/v3?hl=ru
    """
    resource_name = 'analytics'
    version = 'v3'

    def list_accounts(self):
        response = self.client.management().accounts().list().execute()
        return GoogleListResponse(response)

    def list_webproperties(self, account_id):
        response = self.client.management().webproperties().list(
            accountId=account_id
        ).execute()

        return GoogleListResponse(response)

    def list_profiles(self, account_id, webproperty_id):
        response = self.client.management().profiles().list(
            accountId=account_id,
            webPropertyId=webproperty_id
        ).execute()

        return GoogleListResponse(response)

    def list_data_sources(self, account_id, webproperty_id):
        response = self.client.management().customDataSources().list(
            accountId=account_id,
            webPropertyId=webproperty_id
        ).execute()

        return GoogleListResponse(response)

    def list_dimensions(self, account_id, webproperty_id):
        response = self.client.management().customDimensions().list(
            accountId=account_id,
            webPropertyId=webproperty_id
        ).execute()

        return GoogleListResponse(response)

    def data_request(self,
                     profile_id: str,
                     metrics: List[str],
                     dimensions: List[str],
                     start_date: date,
                     end_date: date,
                     filters: List[str],
                     is_accessed_sampling=True,
                     sampling_level='HIGHER_PRECISION',
                     max_results=9999,
                     batch_limit=0):
        """ Executes request to Google Analytics for data.

        :param profile_id:
        :param metrics:
        :param dimensions:
        :param start_date:
        :param end_date:
        :param filters:
        :param is_accessed_sampling:
        :param sampling_level:
        :param max_results:
        :param batch_limit:

        :rtype: list
        """
        if len(dimensions) > 7:
            raise Exception('Only 8 dimensions are allowed')

        params = dict(
            ids=f'ga:{profile_id}',
            max_results=max_results,
            samplingLevel=sampling_level,
            metrics=','.join(metrics),
            dimensions=','.join(dimensions),
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            filters=';'.join(filters),
        )
        first_response = self.client.data().ga().get(**params).execute(num_retries=3)
        total_results = first_response['totalResults']

        if not is_accessed_sampling and first_response['containsSampledData']:
            raise Exception(f'Contains sampled data. Request: {params}')

        yield from first_response.get('rows', [])

        if batch_limit == 1:
            logging.info(f'Received {total_results} records')

        elif total_results > first_response['itemsPerPage']:
            params['start_index'] = max_results - 1
            while True:
                response = self.client.data().ga().get(**params).execute(num_retries=3)

                start_index = response['query']['start-index']

                yield from response['rows']

                cur_index = max_results + start_index
                if total_results > cur_index and batch_limit != start_index // max_results:
                    params['start_index'] = cur_index
                else:
                    break
