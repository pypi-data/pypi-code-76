import time
from typing import Union

import requests
from keycloak import KeycloakOpenID


class KeycloakAuthorizedAPI:
    """
    Util for work with api through keycloak authorization
    """

    __username: str
    __password: str
    __api_url: str
    __keycloak_client: KeycloakOpenID
    __token: Union[dict, None] = None
    __token_expire_at: int = None
    __refresh_token_expire_at: int = None
    __request_retrying: bool = False

    def __init__(
        self,
        keycloak_url: str,
        api_url: str,
        realm: str,
        client_id: str,
        username: str,
        password: str,
    ):
        self.keycloak_client = KeycloakOpenID(
            server_url=keycloak_url,
            realm_name=realm,
            client_id=client_id,
        )
        self.__username = username
        self.__password = password
        self.__api_url = api_url

    def __get_api_url(self, uri: str) -> str:
        return f"{self.__api_url}/{uri}"

    def __is_token_expired(self) -> bool:
        return (self.__token_expire_at is None) or (
            int(time.time()) >= self.__token_expire_at
        )

    def __is_refresh_token_expired(self) -> bool:
        return (self.__refresh_token_expire_at is None) or (
            int(time.time()) >= self.__refresh_token_expire_at
        )

    def __set_token(self, token: dict) -> None:
        self.__token = token
        now = int(time.time())
        self.__token_expire_at = now + token.get("expires_in") - 5
        self.__refresh_token_expire_at = now + token.get("refresh_expires_in") - 5

    def __get_token(self) -> dict:
        if self.__token is None:
            self.__set_token(
                self.keycloak_client.token(
                    username=self.__username, password=self.__password
                )
            )
        return self.__token

    def __refresh_token(self) -> dict:
        # if refresh token expired by time
        # then request new token by username/password
        if self.__is_refresh_token_expired():
            self.__token = None
            self.__get_token()
        else:
            self.__set_token(
                self.keycloak_client.refresh_token(
                    self.__get_token().get("refresh_token")
                )
            )
        return self.__token

    def __get_auth_headers(self) -> dict:
        # if token expired by time
        # then request new token
        if self.__is_token_expired():
            self.__refresh_token()

        return {"Authorization": "Bearer " + self.__get_token().get("access_token")}

    def __api_request(
        self, method: str, uri: str, params: dict = (), data: dict = ()
    ) -> dict:
        response = requests.request(
            method,
            self.__get_api_url(uri),
            headers=self.__get_auth_headers(),
            params=params,
            json=data,
        )

        # if token expired or invalidated
        # then reset them and retry
        if (
            self.__request_retrying is False
            and response.status_code == 401
            and 'error="invalid_token"' in response.headers.get("WWW-Authenticate")
        ):
            self.__token = None
            self.__request_retrying = True
            return self.__api_request(method, uri, params, data)

        self.__request_retrying = False

        if not response.reason:
            try:
                response.reason = response.json()
            finally:
                pass

        response.raise_for_status()
        return response.json()

    def get(self, uri: str, params: dict = ()) -> dict:
        """
        Send GET request
        :param uri: relative from `api_url` path
        :param params: query string params
        :return: response JSON dict
        """
        return self.__api_request("GET", uri, params=params)

    def post(self, uri: str, data: dict, params: dict = ()) -> dict:
        """
        Send POST request
        :param uri: relative from `api_url` path
        :param data: JSON payload
        :param params: query string params
        :return: response JSON dict
        """
        return self.__api_request("POST", uri, params=params, data=data)
