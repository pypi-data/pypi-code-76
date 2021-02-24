import json
from .BaseObject import BaseObject
class Policy(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.id = None
    self.name = None
    self.short_description = None
    self.description = None
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['id']
    if 'name' in d:
      self.name = d['name']
    if 'short_description' in d:
      self.short_description = d['short_description']
    if 'description' in d:
      self.description = d['description']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    d['short_description'] = self.short_description
    d['description'] = self.description
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def load(self):
    obj = self.http_get("/api/v2/policies/" + str(self.id) + ".json")
    self.from_dict(obj)
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      return self.update()
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/policies.json", d)
    self.from_dict(out)
  

    
  def update(self):
    d = self.to_dict()
    self.http_put("/api/v2/policies/" + str(self.id) + ".json", d)
  

    
  def delete(self):
    self.http_delete("/api/v2/policies/" + str(self.id) + ".json")
  

    
  def policy_versions(self):
    obj = self.http_get("/api/v2/policies/" + str(self.id) + "/versions.json")
    the_list = PolicyVersionList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = PolicyVersion(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "version" in x:
        elem.version = x["version"]
      if "tag" in x:
        elem.tag = x["tag"]
      the_list.append(elem)
    return the_list
  

    
  def add_file_check(self, section, file_path, attr, check, expected, absent_pass=False):
    url = "/api/v2/policies/" + str(self.id) + "/add_file_check.json?section=" + str(section) + "&file_path=" + str(file_path) + "&attr=" + str(attr) + "&check=" + str(check) + "&expected=" + str(expected) + "&absent_pass=" + str(absent_pass) + ""
    obj = self.http_post(url, None)
    return obj
  

