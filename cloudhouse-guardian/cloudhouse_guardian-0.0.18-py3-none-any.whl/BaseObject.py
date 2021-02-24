import requests
import json
import urllib3
class BaseObject:
  def from_dict(self, d):
    if 'appliance_url' in d:
      self.appliance_url = d['appliance_url']
    if 'appliance_api_key' in d:
      self.appliance_api_key = d['appliance_api_key']
    if 'sec_key' in d:
      self.sec_key = d['sec_key']
    if 'insecure' in d:
      self.insecure = d['insecure']
  def to_dict(self):
    d = {}
    d['appliance_url'] = self.appliance_url
    d['appliance_api_key'] = self.appliance_api_key
    d['sec_key'] = self.sec_key
    d['insecure'] = self.insecure
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    if appliance_url.startswith("http://") or appliance_url.startswith("https://"):
      # all good
      pass
    else:
      appliance_url = "https://" + appliance_url
    self.appliance_url = appliance_url
    self.appliance_api_key = appliance_api_key
    self.sec_key = sec_key
    self.insecure = insecure
    if insecure:
      urllib3.disable_warnings()
  

    
  def make_headers(self):
    return {
      'Authorization': 'Token token="' + str(self.appliance_api_key) + str(self.sec_key) + '"',
      'Content-Type': 'application/json'
    }
  

    
  def http_get(self, path):
    url = str(self.appliance_url) + path
    headers = self.make_headers()
    response = requests.get(url, headers=headers, verify=(self.insecure==False))
    if response.status_code != 200:
      raise Exception(str(response.status_code) + ":" + response.text)
    return response.json()
  

    
  def http_post(self, path, body):
    url = str(self.appliance_url) + str(path)
    headers = self.make_headers()
    response = requests.post(url, data=json.dumps(body), headers=headers, verify=(self.insecure==False))
    if response.status_code == 200 or response.status_code == 201:
      return response.json()
    if response.status_code == 204:
      return True
    raise Exception(str(response.status_code) + ": " + response.text)
  

    
  def http_put(self, path, body):
    url = str(self.appliance_url) + str(path)
    headers = self.make_headers()
    response = requests.put(url, data=json.dumps(body), headers=headers, verify=(self.insecure==False))
    if response.status_code != 204:
      raise Exception(response.text)
  

    
  def http_delete(self, path):
    url = str(self.appliance_url) + str(path)
    headers = self.make_headers()
    response = requests.delete(url, headers=headers, verify=(self.insecure==False))
    if response.status_code != 204:
      raise Exception(response.text)
  

