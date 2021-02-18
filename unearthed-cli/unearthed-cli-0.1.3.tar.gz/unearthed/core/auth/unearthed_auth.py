"""Unearthed specific requests Authentication Helper."""
from requests.auth import AuthBase
from unearthed.core.auth.unearthed_cognito import UnearthedCognito


class UnearthedAuth(AuthBase):
    """Attach the Unearthed token to a given Request object."""

    def __init__(self, cognito_session=None):
        """Attach to, or create, a Cognito session."""
        if not cognito_session:
            self.cognito_session = UnearthedCognito()
        else:
            self.cognito_session = cognito_session

    def __call__(self, r):
        """Add Authorization header and return the request."""
        self.cognito_session.check_token()
        r.headers["Authorization"] = f"Bearer {self.cognito_session.id_token}"
        return r
