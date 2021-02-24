import json
from .BaseObject import BaseObject
class EventAction(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.id = None
    self.name = None
    self.status = None
    self.type = None
    self.variables = None
    self.view = None
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['id']
    if 'name' in d:
      self.name = d['name']
    if 'status' in d:
      self.status = d['status']
    if 'type' in d:
      self.type = d['type']
    if 'variables' in d:
      self.variables = d['variables']
    if 'view' in d:
      self.view = d['view']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    d['status'] = self.status
    d['type'] = self.type
    d['variables'] = self.variables
    d['view'] = self.view
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
