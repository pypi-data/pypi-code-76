import json
from .BaseObject import BaseObject
class OperatingSystemFamily(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.id = None
    self.name = None
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['id']
    if 'name' in d:
      self.name = d['name']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def operating_systems(self):
    obj = self.http_get("/api/v2/operating_system_families/" + str(self.id) + "/operating_systems.json")
    the_list = OperatingSystemList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = OperatingSystem(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      the_list.append(elem)
    return the_list
  

