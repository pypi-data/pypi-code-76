import configparser
import os
import pandas as pd
import requests

from typing import Iterator, Optional, Tuple, Union


class DrsClient:
    """
    DRS client for DNAstack's DRS API's.

    :param base_url: Base url to search on
    :param auth: (username, pass) for auth access. Defaults to None
    :param wallet: Token for wallet access. Defaults to None
    :param config_file: Config.ini file that contains drs server variables (see README.md)

    :Example:
        from search_python_client.search import DrsClient\n
        base_url = 'https://drs.covidcloud.ca/ga4gh/drs/v1/'\n
        drs_client = DrsClient(base_url=base_url)
    """
    def __init__(self,
                 base_url: str,
                 auth: Optional[Tuple[str, str]] = None,
                 wallet: Optional[str] = None,
                 config_file: Optional[Union[str, bytes, os.PathLike]] = None):
        self.base_url = base_url
        self.auth = auth
        self.wallet = wallet
        self.config_file = config_file
        self.server_type = None
        self._set_server_type()

    def _check_valid(self, atr):
        return atr is not None

    def _check_conflicts(self):
        # Check that there is only one type of authentication method
        if sum(map(self._check_valid, [self.auth, self.wallet])) > 1:
            raise ValueError('Please choose only one authentication method, user authentication or wallet authentication')

    def _read_config_file(self) -> dict:
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config

    def _config_file_to_atr(self):
        config = self._read_config_file()
        self.auth = (config.get('drs-auth', 'username', fallback=None),
                     config.get('drs-auth', 'password', fallback=None))
        self.wallet = config.get('drs-wallet', 'token', fallback=None)
        self._check_conflicts()

    def _set_server_type(self):
        self._check_conflicts()
        if self.config_file:
            self._config_file_to_atr()

        if self.auth:
            self.server_type = 'auth'

        elif self.wallet:
            self.server_type = 'wallet'

    def __str__(self):
        return f'DrsClient(base_url={self.base_url})'

    def __repr__(self):
        return f'DrsClient(base_url={self.base_url})'

    def _get(self, url: str) -> dict:
        """
        Executes get request and returns dict formatted json response
        :param url: Url to search on
        :returns: dict formatted json response
        :raises HTTPError: If response != 200
        """
        if self.server_type == 'auth':
            response = requests.get(url, auth=self.auth)

        elif self.server_type == 'wallet':
            headers = {'Authorization' : f'Bearer {self.wallet}'}
            response = requests.get(url, headers=headers)

        else:
            response = requests.get(url)

        response.raise_for_status()
        return response.json()

    def get_object_info(self, object_id: str) -> pd.DataFrame:
        """
        List all info associated with object.
        :param object_info: Object id of choice
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200
        """
        return pd.DataFrame.from_dict(
            self._get(os.path.join(self.base_url, 'objects', object_id).replace('\\', '/')),
            orient='index'
        ).T


class SearchClient:
    """
    Search client for DNAstack's search API's.

    :param base_url: Base url to search on
    :param wallet: Token for wallet access. Defaults to None

    :Example:
        from search_python_client.search import SearchClient\n
        base_url = 'https://ga4gh-search-adapter-presto-covid19-public.staging.dnastack.com'\n
        search_client = SearchClient(base_url=base_url)

    """

    def __init__(self, base_url: str, wallet: Optional[str] = None):
        self.base_url = base_url
        self.wallet = wallet

    def __str__(self):
        return f'SearchClient(base_url={self.base_url})'

    def __repr__(self):
        return f'SearchClient(base_url={self.base_url})'

    def _get(self, url: str) -> dict:
        """
        Executes get request and returns dict formatted json response

        :param url: Url to search on
        :returns: dict formatted json response
        :raises HTTPError: If response != 200

        """

        if self.wallet:
            headers = {'Authorization': f'Bearer {self.wallet}'}
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url)

        response.raise_for_status()
        return response.json()

    def _get_paginated(self, url: str) -> Iterator:
        """
        Executes get request for paginated responses

        :param url: Url to search on
        :returns: List of dict formatted json responses
        :raises HTTPError: If response != 200

        """
        basename = os.path.basename(url)
        json_response = self._get(url)
        if json_response.get(basename, None):
            for row in json_response[basename]:
                yield row
        while True:
            try:
                json_response = self._get(json_response['pagination']['next_page_url'])
                if json_response.get(basename, None):
                    for row in json_response[basename]:
                        yield row
            except (KeyError, TypeError):
                break

    def _post(self, url: str, json: dict) -> dict:
        """
        Executes post request and returns dict formatted json response

        :param url: Url to search on
        :param json:  Dict formatted json query
        :returns: dict formatted json response
        :raises HTTPError: If response != 200

        """
        if self.wallet:
            headers = {'Authorization': f'Bearer {self.wallet}'}
            response = requests.post(url, json={'query': json}, headers=headers)
        else:
            response = requests.post(url, json={'query': json})

        response.raise_for_status()
        return response.json()

    def _post_paginated(self, url, json) -> Iterator:
        """
        Executes post request for paginated responses

        :param url: Url to search on
        :param json:  Dict formatted json query
        :returns: List of dict formmated json responses
        :raises HTTPError: If response != 200

        """
        json_response = self._post(url, json=json)
        if json_response.get('data', None):
            for row in json_response['data']:
                yield row
        while True:
            try:
                json_response = self._get(json_response['pagination']['next_page_url'])
                if json_response.get('data', None):
                    for row in json_response['data']:
                        yield row
            except KeyError:
                break

    def get_table_list(self) -> Iterator:
        """
        List all tables associated with the url.

        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        """
        return self._get_paginated(
            os.path.join(self.base_url, 'tables').replace('\\', '/')
        )

    def get_table_info(self, table_name: str) -> pd.DataFrame:
        """
        get all info associated with table_name.

        :param table_name: Table name of choice
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        """
        return pd.DataFrame(
            self._get(os.path.join(self.base_url, 'table', table_name, 'info').replace('\\', '/'))
        )

    def get_table_data(self, table_name: str) -> Iterator:
        """
        Get all data associated with table_name.

        :param table_name: Table name of choice
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        """
        return self._get_paginated(
            os.path.join(self.base_url, 'table', table_name, 'data').replace('\\', '/')
        )

    def search_table(self, query: str) -> Iterator:
        """
        Executes an SQL query on table of choice and returns associated data.

        :param table_name: Table name of choice
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        :Example: query = 'SELECT * FROM coronavirus_dnastack_curated.covid_cloud_staging.annotations LIMIT 1000'

        """
        return self._post_paginated(
            os.path.join(self.base_url, 'search').replace('\\', '/'), query
        )
