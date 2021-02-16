from ..HTTP.Requests import *

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
AUTH_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
BASE_URL = "https://api.hubapi.com/"


class hubspot:
  import json
  from . import associations
  from . import companies
  from . import contacts
  from . import deals
  from . import owners
  from . import products
  from . import lineitems

  def __init__(self, client_id, client_secret, refresh_token):
    self.refresh_token = refresh_token
    post_url = f"{BASE_URL}oauth/v1/token"
    auth_body = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    result = post(post_url, AUTH_HEADERS, auth_body)
    auth_result = result['content']
    HEADERS['Authorization'] = f"Bearer {auth_result['access_token']}"

  # Contains utilities for interacting with the HubSpot API
  def get_token_details(self):
    post_url = f"{BASE_URL}oauth/v1/refresh-tokens/{self.refresh_token}"
    return get(post_url, HEADERS)

  def revoke_token(self):
    post_url = f"{BASE_URL}oauth/v1/refresh-tokens/{self.refresh_token}"
    return delete(post_url, AUTH_HEADERS)
