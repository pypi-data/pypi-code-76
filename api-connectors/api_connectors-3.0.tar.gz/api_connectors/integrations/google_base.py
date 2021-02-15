from datetime import datetime

import httplib2
from apiclient import discovery
from oauth2client.client import OAuth2Credentials


class GoogleBase:
    resource_name: str
    version: str

    def __init__(self, credentials: dict):
        if isinstance(credentials['token_expiry'], str):
            token_expiry = datetime.strptime(credentials['token_expiry'], '%Y-%m-%dT%H:%M:%SZ')
        else:
            token_expiry = credentials['token_expiry']

        self.oauth_creds = OAuth2Credentials(
            credentials['access_token'],
            credentials['client_id'],
            credentials['client_secret'],
            credentials['refresh_token'],
            token_expiry,
            credentials['token_uri'],
            credentials['user_agent'],
            revoke_uri=credentials.get('revoke_uri', None),
            id_token=credentials.get('id_token', None),
            token_response=credentials.get('token_response', None)
        )

        self.oauth_creds.invalid = credentials['invalid']
        self.refresh()
        http_auth = self.oauth_creds.authorize(httplib2.Http(timeout=360))
        self.client = discovery.build(self.resource_name, self.version, http=http_auth)

    def refresh(self):
        if self.oauth_creds.access_token_expired:
            http = httplib2.Http(timeout=360)
            self.oauth_creds.refresh(http)