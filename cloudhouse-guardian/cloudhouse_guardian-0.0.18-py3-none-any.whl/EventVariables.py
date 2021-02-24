import json
from .BaseObject import BaseObject
class EventVariables(BaseObject):
    
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.inner_map = {}
  

    
  def __getitem__(self, key):
    return self.inner_map[key]
  

    
  def __setitem__(self, key, value):
    self.inner_map[key] = value
  

    
  def to_json(self):
    return json.dumps(self.inner_map)
  

    
  def to_dict(self):
    return self.inner_map
  

