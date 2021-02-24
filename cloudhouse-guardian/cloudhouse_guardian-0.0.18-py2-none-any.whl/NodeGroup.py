import json
from .BaseObject import BaseObject
from .NodeGroupUser import NodeGroupUser
from .NodeGroupUserList import NodeGroupUserList
class NodeGroup(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.created_at = None
    self.created_by = None
    self.description = None
    self.diff_notify = None
    self.external_id = None
    self.id = None
    self.name = None
    self.node_rules = None
    self.scan_options = None
    self.search_query = None
    self.status = None
    self.updated_at = None
    self.updated_by = None
  def from_dict(self, d):
    if 'created_at' in d:
      self.created_at = d['created_at']
    if 'created_by' in d:
      self.created_by = d['created_by']
    if 'description' in d:
      self.description = d['description']
    if 'diff_notify' in d:
      self.diff_notify = d['diff_notify']
    if 'external_id' in d:
      self.external_id = d['external_id']
    if 'id' in d:
      self.id = d['id']
    if 'name' in d:
      self.name = d['name']
    if 'node_rules' in d:
      self.node_rules = d['node_rules']
    if 'scan_options' in d:
      self.scan_options = d['scan_options']
    if 'search_query' in d:
      self.search_query = d['search_query']
    if 'status' in d:
      self.status = d['status']
    if 'updated_at' in d:
      self.updated_at = d['updated_at']
    if 'updated_by' in d:
      self.updated_by = d['updated_by']
  def to_dict(self):
    d = {}
    d['created_at'] = self.created_at
    d['created_by'] = self.created_by
    d['description'] = self.description
    d['diff_notify'] = self.diff_notify
    d['external_id'] = self.external_id
    d['id'] = self.id
    d['name'] = self.name
    d['node_rules'] = self.node_rules
    d['scan_options'] = self.scan_options
    d['search_query'] = self.search_query
    d['status'] = self.status
    d['updated_at'] = self.updated_at
    d['updated_by'] = self.updated_by
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def load(self):
    obj = self.http_get("/api/v2/node_groups/" + str(self.id) + ".json")
    self.from_dict(obj)
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      return self.update()
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/node_groups.json", d)
    self.from_dict(out)
  

    
  def update(self):
    d = self.to_dict()
    self.http_put("/api/v2/node_groups/" + str(self.id) + ".json", d)
  

    
  def delete(self):
    self.http_delete("/api/v2/node_groups/" + str(self.id) + ".json")
  

    
  def nodes(self):
    obj = self.http_get("/api/v2/node_groups/" + str(self.id) + "/nodes.json")
    the_list = NodeList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = Node(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      the_list.append(elem)
    return the_list
  

    
  def policy_versions(self):
    obj = self.http_get("/api/v2/node_groups/" + str(self.id) + "/policy_versions.json")
    the_list = PolicyVersionList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = PolicyVersion(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      if "version" in x:
        elem.version = x["version"]
      the_list.append(elem)
    return the_list
  

    
  def users(self):
    obj = self.http_get("/api/v2/node_groups/" + str(self.id) + "/users.json")
    the_list = NodeGroupUserList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = NodeGroupUser(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "email" in x:
        elem.email = x["email"]
      if "user_id" in x:
        elem.user_id = x["user_id"]
      the_list.append(elem)
    return the_list
  

    
  def add_user(self, user_id):
    url = "/api/v2/node_groups/" + str(self.id) + "/add_users.json?user_id=" + str(user_id) + ""
    obj = self.http_post(url, None)
    return obj
  

    
  def remove_user(self, user_id):
    url = "/api/v2/node_groups/" + str(self.id) + "/remove_user.json?user_id=" + str(user_id) + ""
    obj = self.http_put(url, None)
    return obj

