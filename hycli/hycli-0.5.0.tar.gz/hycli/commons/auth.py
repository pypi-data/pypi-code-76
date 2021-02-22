from hycli.commons.request import request_token


class Auth(object):
    def __init__(self, url, username, password, check_up=False):
        """
        Holds attributes related to authenticating hypatos API service.
        """
        self.url = url
        self.username = username
        self.password = password
        self.authentication_endpoint = self.get_auth_endpoints()
        self.token_counter = 0
        self.token = self.get_token()

    def get_auth_endpoints(self):
        if "stage" in self.url:
            return "https://customers.stage.hypatos.ai/auth/realms/hypatos/protocol/openid-connect/token"
        else:
            return "https://customers.hypatos.ai/auth/realms/hypatos/protocol/openid-connect/token"

    def get_token(self, refresh_on_every=50):
        if self.token_counter % refresh_on_every == 0:
            self.refresh_token()
        self.token_counter += 1
        return self.token

    def refresh_token(self):
        if self.username and self.password:
            self.token = request_token(
                self.authentication_endpoint, self.username, self.password
            )
        else:
            self.token = None
