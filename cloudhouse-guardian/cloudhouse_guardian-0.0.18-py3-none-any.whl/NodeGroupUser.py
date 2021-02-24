import json
from .BaseObject import BaseObject
class NodeGroupUser(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.email = None
    self.user_id = None
  def from_dict(self, d):
    if 'email' in d:
      self.email = d['email']
    if 'user_id' in d:
      self.user_id = d['user_id']
  def to_dict(self):
    d = {}
    d['email'] = self.email
    d['user_id'] = self.user_id
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
