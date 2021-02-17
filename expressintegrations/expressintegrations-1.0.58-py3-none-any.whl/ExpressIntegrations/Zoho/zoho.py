from ..HTTP.Requests import *

HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}
AUTH_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
AUTH_URL = 'https://accounts.zoho.com'
BASE_URL = 'https://books.zoho.com/api/v3/{}?organization_id='


class zoho:
  import json
  from . import invoices
  from . import contacts
  from . import customerpayments
  from . import users
  from . import items
  from . import expenses

  def __init__(self, app, client_id, client_secret, refresh_token, organization):
    self.refresh_token = refresh_token
    post_url = f"{AUTH_URL}/oauth/v2/token"
    auth_body = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    result = post(post_url, AUTH_HEADERS, auth_body)
    auth_result = result['content']
    if 'access_token' not in auth_result.keys():
      raise Exception(f"Access token not returned: {result}")
    HEADERS['Authorization'] = f"Bearer {auth_result['access_token']}"

  # Contains utilities for interacting with the Zoho API
  def get_org_details(self):
    post_url = f"https://www.zohoapis.com/crm/v2/org"
    return get(post_url, HEADERS)

  def revoke_token(self):
    post_url = f"{AUTH_URL}/oauth/v2/token/revoke?token={self.refresh_token}"
    return post(post_url, AUTH_HEADERS)
