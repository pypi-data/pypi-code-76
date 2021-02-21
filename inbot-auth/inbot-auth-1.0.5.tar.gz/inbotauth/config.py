import os
import json
from typing import Dict, Optional
from inbotauth.user import put_user


def get_client_secrets() -> Optional[Dict]:
    with open(os.getenv('OIDC_CLIENT_SECRETS')) as f:
        return json.load(f)


class BaseConfig:
    # Application Settings
    SECRET_KEY = os.environ.get('FLASK_OIDC_SECRET_KEY', 'base-dap-config-secret-key')
    WHITELISTED_ENDPOINTS = os.environ.get('FLASK_OIDC_WHITELISTED_ENDPOINTS',
                                           "status,healthcheck,health,login,mslogin,oidc_callback,static")

    # Logging Settings
    LOG_FORMAT = '%(asctime)s.%(msecs)03d [%(levelname)s] %(module)s.%(funcName)s:%(lineno)d (%(process)d:' \
                 + '%(threadName)s) - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
    LOG_LEVEL = 'INFO'

    # OIDC Settings
    OIDC_CLIENT_SECRETS = os.environ.get('OIDC_CLIENT_SECRETS', 'client_secrets.json')
    OIDC_INTROSPECTION_AUTH_METHOD = 'client_secret_post'
    OIDC_ID_TOKEN_COOKIE_SECURE = False

    # Database and Sessions Settings
    SESSION_TYPE = 'sqlalchemy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_OIDC_SQLALCHEMY_DATABASE_URI", 'sqlite:///sessions.db')

    CLIENT_ID = get_client_secrets()['web']['client_id']  # Application (client) ID of app registration

    CLIENT_SECRET = get_client_secrets()['web']['client_secret']  # Placeholder - for use ONLY during testing.
    # In a production app, we recommend you use a more secure method of storing your secret,
    # like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
    # https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
    # CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    # if not CLIENT_SECRET:
    #     raise ValueError("Need to define CLIENT_SECRET environment variable")

    AUTHORITY = get_client_secrets()['web']['issuer']  # For multi-tenant app
    # AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

    # You can find more Microsoft Graph API endpoints from Graph Explorer
    # https://developer.microsoft.com/en-us/graph/graph-explorer
    OIDC_USER_ENDPOINT = get_client_secrets()['web']['userinfo_uri']  # This resource requires no admin consent

    REDIRECT_PATH = "/oidc_callback"  # "/getAToken"  # Used for forming an absolute URL to your redirect URI.
    # The absolute URL must match the redirect URI you set
    # in the app's registration in the Azure portal.

    OVERWRITE_REDIRECT_URI = os.environ.get("OVERWRITE_REDIRECT_URI", False)

    # You can find the proper permission names from this document
    # https://docs.microsoft.com/en-us/graph/permissions-reference
    SCOPE = ["User.ReadBasic.All"]
    # SCOPE = ["openid,email,profile,offline_access"]

    PUT_USER_METHOD = put_user
