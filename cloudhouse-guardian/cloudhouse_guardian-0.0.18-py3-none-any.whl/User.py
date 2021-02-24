import json
from .BaseObject import BaseObject
class User(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.id = None
    self.name = None
    self.surname = None
    self.email = None
    self.role = None
    self.invited = None
    self.last_sign_in_at = None
    self.expiry = None
    self.external_id = None
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['id']
    if 'name' in d:
      self.name = d['name']
    if 'surname' in d:
      self.surname = d['surname']
    if 'email' in d:
      self.email = d['email']
    if 'role' in d:
      self.role = d['role']
    if 'invited' in d:
      self.invited = d['invited']
    if 'last_sign_in_at' in d:
      self.last_sign_in_at = d['last_sign_in_at']
    if 'expiry' in d:
      self.expiry = d['expiry']
    if 'external_id' in d:
      self.external_id = d['external_id']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    d['surname'] = self.surname
    d['email'] = self.email
    d['role'] = self.role
    d['invited'] = self.invited
    d['last_sign_in_at'] = self.last_sign_in_at
    d['expiry'] = self.expiry
    d['external_id'] = self.external_id
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def update_role(self, role):
    url = "/api/v2/users/update_role.json?role=" + str(role) + ""
    obj = self.http_put(url, None)
    return obj

    
  def save(self):
    if self.id == 0 or self.id == None:
      raise Exception("Cannot create a User")
    else:
      return self.update()
  

    
  def update(self):
    d = self.to_dict()
    if "id" in d:
      del d["id"]
    if "email" in d:
      del d["email"]
    if "role" in d:
      del d["role"]
    if "invited" in d:
      del d["invited"]
    if "last_sign_in_at" in d:
      del d["last_sign_in_at"]
    if "expiry" in d:
      del d["expiry"]
    self.http_put("/api/v2/users/" + str(self.id) + ".json", d)
  

