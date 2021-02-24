import json
from .BaseObject import BaseObject
class Job(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.id = None
    self.organisation_id = None
    self.source_id = None
    self.source_name = None
    self.source_type = None
    self.status = None
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['id']
    if 'organisation_id' in d:
      self.organisation_id = d['organisation_id']
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
    d['id'] = self.id
    d['organisation_id'] = self.organisation_id
    d['source_id'] = self.source_id
    d['source_name'] = self.source_name
    d['source_type'] = self.source_type
    d['status'] = self.status
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def tasks(self):
    obj = self.http_get("/api/v2/jobs/{job_id}/tasks.json")
    the_list = TaskList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = Task(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "agent_name" in x:
        elem.agent_name = x["agent_name"]
      if "connection_manager_id" in x:
        elem.connection_manager_id = x["connection_manager_id"]
      if "created_at" in x:
        elem.created_at = x["created_at"]
      if "id" in x:
        elem.id = x["id"]
      if "job_id" in x:
        elem.job_id = x["job_id"]
      if "label" in x:
        elem.label = x["label"]
      if "log" in x:
        elem.log = x["log"]
      if "node_id" in x:
        elem.node_id = x["node_id"]
      if "node_session_id" in x:
        elem.node_session_id = x["node_session_id"]
      if "payload" in x:
        elem.payload = x["payload"]
      if "report" in x:
        elem.report = x["report"]
      if "sequence" in x:
        elem.sequence = x["sequence"]
      if "status" in x:
        elem.status = x["status"]
      if "step_description" in x:
        elem.step_description = x["step_description"]
      if "updated_at" in x:
        elem.updated_at = x["updated_at"]
      if "uuid" in x:
        elem.uuid = x["uuid"]
      the_list.append(elem)
    return the_list
  

