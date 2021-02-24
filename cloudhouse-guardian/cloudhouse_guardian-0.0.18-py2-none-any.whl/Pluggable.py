import json
from .BaseObject import BaseObject
class Pluggable(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.description = None
    self.id = None
    self.name = None
    self.operating_system_family = None
    self.operating_system_family_id = None
    self.operating_system_id = None
    self.script = None
  def from_dict(self, d):
    if 'description' in d:
      self.description = d['description']
    if 'id' in d:
      self.id = d['id']
    if 'name' in d:
      self.name = d['name']
    if 'operating_system_family' in d:
      self.operating_system_family = d['operating_system_family']
    if 'operating_system_family_id' in d:
      self.operating_system_family_id = d['operating_system_family_id']
    if 'operating_system_id' in d:
      self.operating_system_id = d['operating_system_id']
    if 'script' in d:
      self.script = d['script']
  def to_dict(self):
    d = {}
    d['description'] = self.description
    d['id'] = self.id
    d['name'] = self.name
    d['operating_system_family'] = self.operating_system_family
    d['operating_system_family_id'] = self.operating_system_family_id
    d['operating_system_id'] = self.operating_system_id
    d['script'] = self.script
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def load(self):
    obj = self.http_get("/api/v2/pluggables/" + str(self.operating_system_id) + ".json")
    self.from_dict(obj)
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      return self.update()
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/pluggables.json", d)
    self.from_dict(out)
  

    
  def update(self):
    d = self.to_dict()
    if "operating_system_family_id" in d:
      del d["operating_system_family_id"]
    if "operating_system_id" in d:
      del d["operating_system_id"]
    self.http_put("/api/v2/pluggables/" + str(self.operating_system_id) + ".json", d)
  

    
  def delete(self):
    self.http_delete("/api/v2/pluggables/" + str(self.operating_system_id) + ".json")
  

