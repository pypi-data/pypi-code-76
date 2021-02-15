import csv
import json
import logging
from abc import ABC
from datetime import datetime
from time import sleep
from typing import Union

from furl import furl

from api_connectors.templates.base import BaseApi

VERSION = 'v1'


class AppmetricaApi(BaseApi):
    """ Groups all APIs of appmetrica into single object. Adds business logic and authentication layer for the API.

        :arg access_token: access token to use till authentication (can be expired)
        :arg refresh_token:
        :arg expires_in: a time when the access token becomes expired

    Documentation:
        Authorization: https://appmetrica.yandex.ru/docs/mobile-api/intro/authorization.html
        Logs API: https://appmetrica.yandex.ru/docs/mobile-api/logs/about.html
    """

    def __init__(self,
                 access_token: str,
                 refresh_token: str,
                 expires_in: int,
                 client_id: str,
                 client_secret: str,
                 appmetrica_url: Union[str, furl] = 'https://api.appmetrica.yandex.ru/',
                 oauth_url: Union[str, furl] = 'https://oauth.yandex.ru/'):
        super().__init__(appmetrica_url)

        # Separated APIs within the general API resource
        self.auth = YandexAuthApi(
            access_token, refresh_token, expires_in, oauth_url, client_id, client_secret
        )
        self.auth.check_update_token()

        self.logs = AppmetricaLogsApi(appmetrica_url, self.auth)
        self.management = AppmetricaManagementApi(appmetrica_url, self.auth)


class YandexBaseAPI(BaseApi, ABC):
    """ The base API object for all Yandex APIs """
    resource: str

    def __init__(self,
                 base_url: Union[str, furl],
                 oauth_api: 'YandexAuthApi',
                 **kwargs):
        api_url = furl(base_url).set(path=f'/{self.resource}/{VERSION}')
        kwargs['base_url'] = api_url

        super().__init__(**kwargs)

        self.oauth_api = oauth_api
        self.headers['Authorization'] = f'OAuth {self.oauth_api.access_token}'

    def paginate_request(self, method: str, url: furl, params: dict):
        """ THere is no pagination in Yandex! """
        ready_url = furl(url).add(query_params=params)
        response: str = self.make_request(method, ready_url, encode='x-www-form-urlencoded')
        return response


class YandexAuthApi(BaseApi):
    """ Implements OAuth API (Passport) of Yandex services """

    def __init__(self,
                 access_token: str,
                 refresh_token: str,
                 expires_in: int,
                 base_url: Union[str, furl],
                 client_id: str,
                 client_secret: str):
        super().__init__(base_url)

        self.client_id = client_id
        self.client_secret = client_secret
        self.expires_in = expires_in
        self.refresh_token = refresh_token
        self.access_token = access_token

        self.headers = dict(Host=self.host)

    def update_token(self):
        now = datetime.now().timestamp()
        url = furl(self.base_url).add(path='token')
        body = dict(
            grant_type='refresh_token', refresh_token=self.refresh_token, client_id=self.client_id,
            client_secret=self.client_secret
        )

        response: dict = self.make_request('POST', url, data=body, encode='x-www-form-urlencoded')

        self.access_token = response['access_token']
        self.expires_in = now + response['expires_in']

        return self.access_token

    def check_update_token(self):
        now = datetime.now().timestamp()

        if now > self.expires_in:
            return self.update_token()


class AppmetricaManagementApi(YandexBaseAPI):
    """ Implements Management API section of Appmetrica

    Documentation: https://appmetrica.yandex.ru/docs/mobile-api/management/about.html
    """
    resource = 'management'

    def applications_list(self):
        url = furl(self.base_url).add(path='applications')
        response: dict = self.make_request('GET', url)
        return response


class AppmetricaLogsApi(YandexBaseAPI):
    """ Implements Logs API section of Appmetrica

    Documentation: https://appmetrica.yandex.ru/docs/mobile-api/logs/about.html
    """
    resource = 'logs'
    dt_fmt = '%Y-%m-%d %H:%M:%S'

    def export(self,
               log_name: str,
               application_id: int,
               start_date: datetime,
               end_date: datetime,
               fields: list,
               fmt='csv',
               limit=None,
               waiting_iterations=20):
        """ Exporting any kind of Yandex Logs
        :param log_name: could be: {events, installations, profiles, errors, crashes, revenue_events, ...}
        :param application_id: could be received from
        :param start_date:
        :param end_date:
        :param fields: looking at: https://appmetrica.yandex.ru/docs/mobile-api/logs/ref/events.html and not only events
        :param fmt: {csv, json}
        :param limit: could be any number, if you need a cut report
        :param waiting_iterations:
        :return:
        """
        params = dict(
            application_id=application_id,
            date_since=start_date.strftime(self.dt_fmt),
            date_until=end_date.strftime(self.dt_fmt),
            fields=','.join(fields or [])
        )

        if limit:
            params['limit'] = limit

        url = furl(self.base_url).add(
            path=f'/export/{log_name}.{fmt}',
            query_params=params
        )

        max_i = i = waiting_iterations
        data_sheet = None
        while i:
            i -= 1
            response: str = self.make_request('GET', url, encode='x-www-form-urlencoded')

            if response == 'Your query is added to the queue.':
                sleep_time = 2 ** (max_i - i)
                logging.info(f'Sleeping for {sleep_time} seconds')
                sleep(sleep_time)
            else:
                logging.info('The data received')

                if fmt == 'csv':
                    reader = csv.reader(response.split('\n'))
                    header = next(reader)
                    data_sheet = [dict(zip(header, row)) for row in reader]
                else:
                    data_sheet = json.loads(response)

        if not data_sheet:
            raise TimeoutError('Couldn\'t wait for an response')

        return data_sheet
