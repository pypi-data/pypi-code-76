import requests

from typing import List, Tuple

from .__user_config import EnvironmentConfiguration


class Client:
    """
        class for communication with the Maquette Hub API
    """
    __base_url: str = None
    __headers: dict

    def __init__(self, base_url: str, user_id: str, roles: List):
        self.__base_url = base_url
        self.__headers = {
            'x-user-id': user_id,
            'x-user-roles': ','.join(roles)
        }

    @staticmethod
    def from_config(config: EnvironmentConfiguration) -> 'Client':
        """
            initialize Client object from UserConfiguration
        Args:
            config: UserConfiguration object with informations about the url, user and its roles

        Returns: initiated Client object

        """
        return Client(config.get_url(), config.get_user(), config.get_roles())

    def command(self, cmd: str, args: dict = None, headers: dict = None) -> Tuple[int, dict]:
        """
            main communication function between client and Maquette Hub API for sending commands

        Args:
            cmd: str for the actual cmd
            args: dict for additional json arguments
            headers: dict for header parameters

        Returns: Tuple with the result status code and the content of the response if the status code is in between 200 and 299

        """
        request_body = {'command': cmd}
        if args:
            request_body.update(args)
        if headers:
            headers = {**self.__headers, **headers}
        else:
            headers = self.__headers
        response = requests.post(self.__base_url + 'commands', json=request_body, headers=headers)
        if response.status_code < 200 or response.status_code > 299:

            raise RuntimeError("call to Maquette controller was not successful ¯\\_(ツ)_/¯\n"
                               "status code: " + str(response.status_code) + ", content:\n" + response.text)
        else:
            if (("Accept", "application/csv") in headers.items()) or (("Accept", "text/plain") in headers.items()):
                result = response.content
            else:
                result = response.json()
            return response.status_code, result

    def get(self, url: str, headers=None) -> requests.Response:
        """
            function to access Data Assets as JSON Objects
        Args:
            url: additional url path, to be added to the base_url according to the Data Asset type
            headers: dict for header parameters

        Returns: Response Content as JSON Object

        """
        if headers:
            headers = {**self.__headers, **headers}
        else:
            headers = self.__headers
        response = requests.get(self.__base_url + url, headers=headers)
        if response.status_code < 200 or response.status_code > 299:
            raise RuntimeError("call to Maquette controller was not successful ¯\\_(ツ)_/¯\n"
                               "status code: " + str(response.status_code) + ", content:\n" + response.text)
        else:
            return response

    def put(self, url: str, json=None, files=None, headers=None) -> requests.Response:
        """
            function to upload Data Asset objects
        Args:
            url: additional url path, to be added to the base_url according to the Data Asset type
            json: dict of json parameters
            files: binary objects to be uploaded
            headers: dict for header parameters

        Returns: Response Content as JSON Object

        """
        if headers:
            headers = {**self.__headers, **headers}
        else:
            headers = self.__headers
        response = requests.put(self.__base_url + url, json=json, files=files, headers=headers)
        if response.status_code < 200 or response.status_code > 299:
            raise RuntimeError("call to Maquette controller was not successful ¯\\_(ツ)_/¯\n"
                               "status code: " + str(response.status_code) + ", content:\n" + response.text)
        else:
            return response

    def post(self, url: str, json=None, files=None, headers=None) -> requests.Response:
        """
            function to upload Data Asset objects
        Args:
            url: additional url path, to be added to the base_url according to the Data Asset type
            json: dict of json parameters
            files: binary objects to be uploaded
            headers: dict for header parameters

        Returns: Response Content as JSON Object

        """
        if headers:
            headers = {**self.__headers, **headers}
        else:
            headers = self.__headers
        response = requests.post(self.__base_url + url, json=json, files=files, headers=headers)
        if response.status_code < 200 or response.status_code > 299:
            raise RuntimeError("call to Maquette controller was not successful ¯\\_(ツ)_/¯\n"
                               "status code: " + str(response.status_code) + ", content:\n" + response.text)
        else:
            return response
