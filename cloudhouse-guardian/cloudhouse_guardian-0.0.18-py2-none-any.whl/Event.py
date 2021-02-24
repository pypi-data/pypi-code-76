import json
from .BaseObject import BaseObject
class Event(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.id = None
    self.type_id = None
    self.environment_id = None
    self.created_at = None
    self.variables = EventVariables(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['id']
    if 'type_id' in d:
      self.type_id = d['type_id']
    if 'environment_id' in d:
      self.environment_id = d['environment_id']
    if 'created_at' in d:
      self.created_at = d['created_at']
    if 'variables' in d:
      self.variables = d['variables']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['type_id'] = self.type_id
    d['environment_id'] = self.environment_id
    d['created_at'] = self.created_at
    d['variables'] = self.variables
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def environment(self):
    obj = self.http_get("/api/v2/environments/" + str(self.environment_id) + ".json")
    elem = Environment(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    elem.organisation_id = obj["organisation_id"]
    elem.short_description = obj["short_description"]
    elem.node_rules = obj["node_rules"]
    return elem
  

