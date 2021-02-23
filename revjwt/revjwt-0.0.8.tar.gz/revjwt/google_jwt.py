from google.oauth2 import id_token
from google.auth.transport import requests


def decode(token, client_id):
    request = requests.Request()
    
    id_info = id_token.verify_oauth2_token(
        token, request, client_id)
    
    if id_info['iss'] != 'accounts.google.com':
        raise ValueError('Wrong issuer.')

    return id_info
