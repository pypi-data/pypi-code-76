import json
from .BaseObject import BaseObject
from .EventVariables import EventVariables
class ExternalEvent(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.type = None
    self.variables = EventVariables(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
  def from_dict(self, d):
    if 'type' in d:
      self.type = d['type']
    if 'variables' in d:
      self.variables = d['variables']
  def to_dict(self):
    d = {}
    d['type'] = self.type
    d['variables'] = self.variables
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def create(self):
    d = {}
    d["variables"] = self.variables.to_dict()
    d["variables"]["type"] = self.type
    self.http_post("/api/v2/events.json", d)
  

