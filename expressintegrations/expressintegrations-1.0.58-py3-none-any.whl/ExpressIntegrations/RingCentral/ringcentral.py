from ringcentral import SDK
from ..Utils import Utils
import time


BASE_URL = 'https://platform.ringcentral.com'


class ringcentral:
  def __init__(self, client_id, client_secret, username, password, extension, server_url=BASE_URL):
    rcsdk = SDK(client_id, client_secret, server_url)
    self.platform = rcsdk.platform()
    self.extension = extension
    self.platform.login(username, extension, password)
    self.account_id = self.get_account_details().json().id

  # Contains utilities for interacting with the MailChimp api
  def get_account_details(self, account_id='~'):
    result = self.platform.get(f"/restapi/v1.0/account/{account_id}")
    wait = 1
    while Utils.is_retryable(result.response().status_code):
      print(f"retrying. last result: {result}")
      time.sleep(wait)
      wait = wait * 2 if wait < 10 else 10
      result = self.platform.get(f"/restapi/v1.0/account/{account_id}")
    if not result.ok:
      raise Exception(f"Failed to get account details. Result: {result.error()}")
    return result

  def send_sms(self, sender_number, recipient_number, text, extension='~'):
    post_body = {
        'from': {
            'phoneNumber': sender_number
        },
        'to': [
            {
                'phoneNumber': recipient_number
            }
        ],
        'text': text
    }
    result = self.platform.post(f"/restapi/v1.0/account/~/extension/{extension}/sms", post_body)
    wait = 1
    while Utils.is_retryable(result.response().status_code):
      print(f"retrying. last result: {result}")
      time.sleep(wait)
      wait = wait * 2 if wait < 10 else 10
      result = self.platform.post(f"/restapi/v1.0/account/~/extension/{extension}/sms", post_body)
    if not result.ok:
      raise Exception(f"Failed to send sms. Result: {result.error()}")
    return result

  def renew_webhook(self, subscription_id):
    result = self.platform.post(f"/restapi/v1.0/subscription/{subscription_id}/renew")
    wait = 1
    while Utils.is_retryable(result.response().status_code):
      print(f"retrying. last result: {result}")
      time.sleep(wait)
      wait = wait * 2 if wait < 10 else 10
      result = self.platform.post(f"/restapi/v1.0/subscription/{subscription_id}/renew")
    if not result.ok:
      raise Exception(f"Failed to renew webhook. Result: {result.error()}")
    return result

  def create_contact(self, contact, dialing_plan=None):
    query_params = {}
    if dialing_plan is not None:
      query_params['dialingPlan'] = dialing_plan
    result = self.platform.post(f"/restapi/v1.0/account/~/extension/~/address-book/contact", contact, query_params)
    wait = 1
    while Utils.is_retryable(result.response().status_code):
      print(f"retrying. last result: {result}")
      time.sleep(wait)
      wait = wait * 2 if wait < 10 else 10
      result = self.platform.post(f"/restapi/v1.0/account/~/extension/~/address-book/contact", contact, query_params)
    if not result.ok:
      raise Exception(f"Failed to create contact. Result: {result.error()}")
    return result

  def get_contacts(self, starts_with=None, sort_by=None, page=None, per_page=None, phone_number=None):
    query_params = {}
    if starts_with is not None:
      query_params['startsWith'] = starts_with
    if sort_by is not None:
      query_params['sortBy'] = sort_by
    if page is not None:
      query_params['page'] = page
    if per_page is not None:
      query_params['perPage'] = per_page
    if phone_number is not None:
      query_params['phoneNumber'] = phone_number
    result = self.platform.get(f"/restapi/v1.0/account/~/extension/~/address-book/contact", query_params)
    wait = 1
    while Utils.is_retryable(result.response().status_code):
      print(f"retrying. last result: {result}")
      time.sleep(wait)
      wait = wait * 2 if wait < 10 else 10
      result = self.platform.get(f"/restapi/v1.0/account/~/extension/~/address-book/contact", query_params)
    if not result.ok:
      raise Exception(f"Failed to search contacts. Result: {result.error()}")
    return result

  def get_contact(self, contact_id):
    result = self.platform.get(f"/restapi/v1.0/account/~/extension/~/address-book/contact/{contact_id}")
    wait = 1
    while Utils.is_retryable(result.response().status_code):
      print(f"retrying. last result: {result}")
      time.sleep(wait)
      wait = wait * 2 if wait < 10 else 10
      result = self.platform.get(f"/restapi/v1.0/account/~/extension/~/address-book/contact/{contact_id}")
    if not result.ok:
      raise Exception(f"Failed to get contact. Result: {result.error()}")
    return result

  def update_contact(self, contact_id, contact, dialing_plan=None):
    query_params = {}
    if dialing_plan is not None:
      query_params['dialingPlan'] = dialing_plan
    result = self.platform.put(f"/restapi/v1.0/account/~/extension/~/address-book/contact/{contact_id}", contact, query_params)
    wait = 1
    while Utils.is_retryable(result.response().status_code):
      print(f"retrying. last result: {result}")
      time.sleep(wait)
      wait = wait * 2 if wait < 10 else 10
      result = self.platform.put(f"/restapi/v1.0/account/~/extension/~/address-book/contact/{contact_id}", contact, query_params)
    if not result.ok:
      raise Exception(f"Failed to update contact. Result: {result.error()}")
    return result

  def delete_contact(self, contact_id):
    result = self.platform.delete(f"/restapi/v1.0/account/~/extension/~/address-book/contact/{contact_id}")
    wait = 1
    while Utils.is_retryable(result.response().status_code):
      print(f"retrying. last result: {result}")
      time.sleep(wait)
      wait = wait * 2 if wait < 10 else 10
      result = self.platform.delete(f"/restapi/v1.0/account/~/extension/~/address-book/contact/{contact_id}")
    if not result.ok:
      raise Exception(f"Failed to delete contact. Result: {result.error()}")
    return result

  def search_company_directory(self, search_string=None, show_federated=True, extension_type=None, order_by=None, page=None, per_page=None):
    post_body = {}
    if search_string is not None:
      post_body['searchString'] = search_string
    post_body['showFederated'] = show_federated
    if extension_type is not None:
      post_body['extensionType'] = extension_type
    if order_by is not None:
      post_body['orderBy'] = order_by
    if page is not None:
      post_body['page'] = page
    if per_page is not None:
      post_body['perPage'] = per_page
    result = self.platform.post(f"/restapi/v1.0/account/~/directory/entries/search", post_body)
    wait = 1
    while Utils.is_retryable(result.response().status_code):
      print(f"retrying. last result: {result}")
      time.sleep(wait)
      wait = wait * 2 if wait < 10 else 10
      result = self.platform.post(f"/restapi/v1.0/account/~/directory/entries/search", post_body)
    if not result.ok:
      raise Exception(f"Failed to search company directory. Result: {result.error()}")
    return result
