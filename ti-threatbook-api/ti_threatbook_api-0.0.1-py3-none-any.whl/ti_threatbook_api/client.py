"""
ti-threatbook-api.client
~~~~~~~~~~~~~

This module implements the ThreatBook API.

:copyright: (c) 2021 - by yege0201
"""
import requests

from .exception import APIError


class ThreatBook:
    """Wrapper around the ThreatBook REST APIs

    :param key: The ThreatBook API key that can be obtained from your account page (https://x.threatbook.cn/nodev4/vb4/myAPI)
    :type key: str
    """

    def __init__(self, key):
        """Initializes the API object.

        :param key: The ThreatBook API key.
        :type key: str
        """
        self.api_key = key
        self.base_url = 'https://api.threatbook.cn/v3'
        self._session = requests.Session()

    def _request(self, function, params, method: str = 'get'):
        """General-purpose function to create web requests to ThreatBook.

        Arguments:
            function  -- name of the function you want to execute
            params    -- dictionary of parameters for the function
            method    -- http request methods, only permit 'get' or 'post'

        Returns
            A dictionary containing the function's results.

        """
        # Add the API key parameter automatically
        params['apikey'] = self.api_key

        # Define the response error codes
        error_codes = [6, 8, -1, -2, -3, -4, -5]

        base_url = self.base_url

        # Send the request
        try:
            method = method.lower()
            if method == 'post':
                data = self._session.post(base_url + function, params)
            else:
                data = self._session.get(base_url + function, params=params)
        except Exception:
            raise APIError('Unable to connect to ThreatBook')

        # Check that the API key wasn't rejected
        try:
            response_code = data.json().get('response_code')
        except:
            response_code = -5
        if response_code in error_codes:
            try:
                # Return the actual error message if the API returned valid JSON
                error = data.json()['verbose_msg']
            except Exception as e:
                # Otherwise lets raise the error message
                error = '{}'.format(e)
            raise APIError(error)

        # Parse the text into JSON
        try:
            data = data.json()
        except ValueError:
            raise APIError('Unable to parse JSON response')

        # Return the data
        return data

    def ip_query(self, resource: str, lang: str = 'en'):
        """Analyze IP address intelligence information.

        :param resource: IP Address, single IP supported
        :type resource: str
        :param lang: (optional) Language of return results
        :type lang: str

        :returns: A dictionary containing the function's results.
        """
        args = {
            'resource': resource,
            'lang': lang
        }

        return self._request(function='/ip/query', params=args, method='post')

    def domain_query(self, resource: str, lang: str = 'en'):
        """Analyze domain name intelligence information.

        :param resource: domain name, single domain name supported
        :type resource: str
        :param lang: (optional) Language of return results
        :type lang: str

        :returns: A dictionary containing the function's results.
        """
        args = {
            'resource': resource,
            'lang': lang
        }

        return self._request(function='/domain/query', params=args, method='post')

    def file_report(self, sha256: str):
        """Get the analysis report of the file.

        :param sha256: The sha256 value of the file
        :type sha256: str

        :returns: A dictionary containing the function's results.
        """
        args = {
            'sha256': sha256,
        }

        return self._request(function='/file/report', params=args, method='post')

    def file_report_multiengines(self, sha256: str):
        """Get the anti-virus scan report of the file.

        :param sha256: The sha256 value of the file
        :type sha256: str

        :returns: A dictionary containing the function's results.
        """
        args = {
            'sha256': sha256,
        }

        return self._request(function='/file/report/multiengines', params=args, method='post')

    def scene_dns(self, resource: str, lang: str = 'en'):
        """Risk analysis base on IP or domain name.

        :param resource: IP address or domain name, multiple supported(up to 100), separated by commas(,)
        :type resource: str
        :param lang: (optional) Language of return results
        :type lang: str

        :returns: A dictionary containing the function's results.
        """
        args = {
            'resource': resource,
            'lang': lang
        }

        return self._request(function='/scene/dns', params=args, method='post')

    def scene_domain_context(self, resource: str, lang: str = 'en'):
        """Look up contextual information based on a malicious domain name.

        :param resource: domain name, single domain name supported
        :type resource: str
        :param lang: (optional) Language of return results
        :type lang: str

        :returns: A dictionary containing the function's results.
        """
        args = {
            'resource': resource,
            'lang': lang
        }

        return self._request(function='/scene/domain_context', params=args, method='post')

    def scene_ip_reputation(self, resource: str, lang: str = 'en'):
        """Analysis of reputaion information base on IP address.

        :param resource: IP Address, multiple IPs supported(up to 100), separated by commas(,)
        :type resource: str
        :param lang: (optional) Language of return results
        :type lang: str

        :returns: A dictionary containing the function's results.
        """
        args = {
            'resource': resource,
            'lang': lang
        }

        return self._request(function='/scene/ip_reputation', params=args, method='post')
