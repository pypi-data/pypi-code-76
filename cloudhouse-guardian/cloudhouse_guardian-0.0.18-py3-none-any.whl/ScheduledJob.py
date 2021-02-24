import json
from .BaseObject import BaseObject
class ScheduledJob(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.data = None
    self.id = None
    self.source_id = None
    self.source_name = None
    self.source_type = None
    self.status = None
  def from_dict(self, d):
    if 'data' in d:
      self.data = d['data']
    if 'id' in d:
      self.id = d['id']
    if 'source_id' in d:
      self.source_id = d['source_id']
    if 'source_name' in d:
      self.source_name = d['source_name']
    if 'source_type' in d:
      self.source_type = d['source_type']
    if 'status' in d:
      self.status = d['status']
  def to_dict(self):
    d = {}
    d['data'] = self.data
    d['id'] = self.id
    d['source_id'] = self.source_id
    d['source_name'] = self.source_name
    d['source_type'] = self.source_type
    d['status'] = self.status
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def load(self):
    obj = self.http_get("/api/v2/scheduled_jobs/" + str(self.id) + ".json")
    self.from_dict(obj)
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      return self.update()
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/scheduled_jobs.json", d)
    self.from_dict(out)
  

    
  def update(self):
    d = self.to_dict()
    self.http_put("/api/v2/scheduled_jobs/" + str(self.id) + ".json", d)
  

    
  def delete(self):
    self.http_delete("/api/v2/scheduled_jobs/" + str(self.id) + ".json")
  

    
  def cancel_jobs(self):
    url = "/api/v2/scheduled_jobs/" + str(self.id) + "/cancel_jobs.json"
    obj = self.http_post(url, None)
    return obj
  

