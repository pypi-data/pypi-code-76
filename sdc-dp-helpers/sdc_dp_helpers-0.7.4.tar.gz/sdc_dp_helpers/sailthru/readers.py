"""
    CUSTOM READERS CLASSES
        - Class which manages reader tasks like auth, requests, pagination
"""
import json

from sailthru import SailthruClient


def get_credentials(api_keys_path) -> list:
    with open(api_keys_path) as file:
        data = json.load(file)

    return data.get('api_key'), data.get('api_secret')


class CustomSailThruReader:
    def __init__(self, api_keys_path):
        self.api_keys_path = api_keys_path
        self.api_key, self.api_secret = get_credentials(api_keys_path)


class CustomSailThruReaderOLD():
    """
        Custom SailThru Reader
    """

    # pylint: disable=super-init-not-called
    def __init__(self, api_keys_path: str):
        self.sailthru_client = self.auth_credentials(api_keys_path)

    @staticmethod
    def auth_credentials(
            api_keys_path
    ):
        """
        Create a client to communicate with Sailthru
        Args:
            api_keys_path: The file path to the api key and secret.
        Returns:
            A service that is connected to the specified API.
        """
        with open(api_keys_path) as json_file:
            data = json.load(json_file)

        return SailthruClient(data['api_key'], data['api_secret'])

    def call_api(self, query: dict):
        """
            returns results of API call
        """
        response = self.sailthru_client.api_get(query.get('endpoint'), query.get('parameters')[0])
        if not response.is_ok():
            error = response.get_error()
            raise Exception("APIError: {}, Status Code: {}, Error Code: {}".format(
                error.get_message(),
                str(response.get_status_code()),
                str(error.get_error_code())))
        return response.get_body()
