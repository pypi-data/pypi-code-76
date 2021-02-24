import json
from .BaseObject import BaseObject
class ConnectionManagerGroup(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.api_key = None
    self.id = None
    self.name = None
    self.status = None
  def from_dict(self, d):
    if 'api_key' in d:
      self.api_key = d['api_key']
    if 'id' in d:
      self.id = d['id']
    if 'name' in d:
      self.name = d['name']
    if 'status' in d:
      self.status = d['status']
  def to_dict(self):
    d = {}
    d['api_key'] = self.api_key
    d['id'] = self.id
    d['name'] = self.name
    d['status'] = self.status
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def connection_managers(self):
    obj = self.http_get("/api/v2/connection_manager_groups/" + str(self.id) + "/connection_managers.json")
    the_list = ConnectionManagerList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = ConnectionManager(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      the_list.append(elem)
    return the_list
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      raise Exception("Cannot update a ConnectionManagerGroup")
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/connection_manager_groups.json", d)
    self.from_dict(out)
  

