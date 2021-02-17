import json

from ..HTTP.Requests import *
from ..Utils import Utils
from urllib.parse import urlencode


class ministry:

  def __init__(self, site, access_token):
    self.headers = {"Content-Type": "application/json", "Accept": "application/json"}
    self.headers['Authorization'] = f"Bearer {access_token}"
    self.base_url = site

  def create_record(self, table, record):
    return self.create_records(table, [record])

  def create_records(self, table, records):
    post_url = f"{self.base_url}tables/{table}"
    result = post(post_url, self.headers, json.dumps(records))
    if not Utils.is_success(result['status_code']):
      raise Exception(f"Failed to create record. Result: {result}")
    return result

  def get_record_by_id(self, table, record_id):
    post_url = f"{self.base_url}tables/{table}/{record_id}"
    result = get(post_url, self.headers)
    if not Utils.is_success(result['status_code']):
      raise Exception(f"Failed to retrieve record. Result: {result}")
    return result

  def search_records(self, table, search_string=None, order_by=None):
    post_url = f"{self.base_url}tables/{table}"
    if search_string is not None:
      sql_filter = {'filter': search_string}
      post_url = f"{post_url}?${urlencode(sql_filter)}"

    if order_by is not None:
      sql_order = {'order_by': order_by}
      post_url = f"{post_url}&${urlencode(sql_order)}"
    result = get(post_url, self.headers)
    if not Utils.is_success(result['status_code']):
      raise Exception(f"Failed to retrieve records. Result: {result}")
    return result

  def update_record(self, table, record):
    return self.update_records(table, [record])

  def update_records(self, table, records):
    post_url = f"{self.base_url}tables/{table}"
    result = put(post_url, self.headers, json.dumps(records))
    if not Utils.is_success(result['status_code']):
      raise Exception(f"Failed to update record. Result: {result}")
    return result

  def delete_record(self, table, record_id):
    post_url = f"{self.base_url}tables/{table}/{record_id}"
    result = delete(post_url, self.headers)
    if not Utils.is_success(result['status_code']):
      raise Exception(f"Failed to delete record. Result: {result}")
    return result
