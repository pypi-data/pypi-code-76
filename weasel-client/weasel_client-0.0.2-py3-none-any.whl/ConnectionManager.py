import requests

from weasel_client.Exceptions import InvalidTokenException, ConnectionException


class ConnectionManager:
    """
    Singleton-Baseclass for the ConnectionManager
    """
    instance = None

    def __init__(self, token, url):
        if ConnectionManager.instance is None:
            ConnectionManager.instance = ConnectionManager.__ConnectionManager(token=token, url=url)

    @staticmethod
    def destruct():
        """
        Clears the instance on ConnectionManager-destruction
        """
        ConnectionManager.instance = None

    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __ConnectionManager:
        """
        Singleton for connections to the WEASEL-API
        """
        token = None
        api_url = None

        def __init__(self, token, url):
            self.api_url = url
            self.token = token

        def get_token(self):
            """
            Returns the API-Token
            """
            return self.token

        def _set_token(self, token):
            """
            Sets the API-Token
            :param token: new API-Token
            """
            self.token = token

        def url(self):
            """
            returns the API-URL
            """
            return self.api_url

        def get(self, request):
            """
            Requests some result from the WEASEL-API and returns it
            :param request: Request-URL
            """
            if self.token is None:
                raise InvalidTokenException(
                    "No token given! Set the token using the 'set_token'-Method.")
            headers = {
                'Authorization': "Token " + self.token
            }
            if not request.startswith(self.api_url):
                request = self.api_url + request
            answer = requests.get(request, headers=headers)
            if answer.status_code == 200:
                return answer
            elif answer.status_code == 404 or answer.status_code == 500:
                raise ConnectionException("Could not connect to WEASEL API.")
            elif answer.status_code == 401:
                raise InvalidTokenException(
                    "Invalid token: '" + self.token + "'! Could not connect to WEASEL API.")
            else:
                raise ConnectionException(
                    "Unknown connection error. Status code: " + str(answer.status_code))

        def connected(self):
            """
            Simple check if the Connection Manager can connect to the WEASEL-API
            """
            try:
                self.get(request="")
                return True
            except (InvalidTokenException, ConnectionException):
                return False
