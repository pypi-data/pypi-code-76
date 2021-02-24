import json
from .BaseObject import BaseObject
class Environment(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.description = None
    self.id = None
    self.name = None
    self.node_rules = None
    self.short_description = None
    self.updated_by = None
    self.created_by = None
    self.updated_at = None
    self.created_at = None
    self.weight = None
  def from_dict(self, d):
    if 'description' in d:
      self.description = d['description']
    if 'id' in d:
      self.id = d['id']
    if 'name' in d:
      self.name = d['name']
    if 'node_rules' in d:
      self.node_rules = d['node_rules']
    if 'short_description' in d:
      self.short_description = d['short_description']
    if 'updated_by' in d:
      self.updated_by = d['updated_by']
    if 'created_by' in d:
      self.created_by = d['created_by']
    if 'updated_at' in d:
      self.updated_at = d['updated_at']
    if 'created_at' in d:
      self.created_at = d['created_at']
    if 'weight' in d:
      self.weight = d['weight']
  def to_dict(self):
    d = {}
    d['description'] = self.description
    d['id'] = self.id
    d['name'] = self.name
    d['node_rules'] = self.node_rules
    d['short_description'] = self.short_description
    d['updated_by'] = self.updated_by
    d['created_by'] = self.created_by
    d['updated_at'] = self.updated_at
    d['created_at'] = self.created_at
    d['weight'] = self.weight
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def load(self):
    obj = self.http_get("/api/v2/environments/" + str(self.id) + ".json")
    self.from_dict(obj)
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      return self.update()
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/environments.json", d)
    self.from_dict(out)
  

    
  def update(self):
    d = self.to_dict()
    if "id" in d:
      del d["id"]
    if "organisation_id" in d:
      del d["organisation_id"]
    if "updated_by" in d:
      del d["updated_by"]
    if "created_by" in d:
      del d["created_by"]
    if "updated_at" in d:
      del d["updated_at"]
    if "created_at" in d:
      del d["created_at"]
    if "weight" in d:
      del d["weight"]
    self.http_put("/api/v2/environments/" + str(self.id) + ".json", d)
  

    
  def delete(self):
    self.http_delete("/api/v2/environments/" + str(self.id) + ".json")
  

    
  def nodes(self):
    obj = self.http_get("/api/v2/environments/" + str(self.id) + "/nodes.json")
    the_list = NodeList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = Node(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      the_list.append(elem)
    return the_list
  

