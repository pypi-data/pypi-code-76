import json
from .BaseObject import BaseObject
class NodeScan(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.associated_id = None
    self.category = None
    self.created_at = None
    self.data = None
    self.id = None
    self.label = None
    self.node_id = None
    self.scan_options = None
    self.task_id = None
    self.tsv = None
    self.updated_at = None
  def from_dict(self, d):
    if 'associated_id' in d:
      self.associated_id = d['associated_id']
    if 'category' in d:
      self.category = d['category']
    if 'created_at' in d:
      self.created_at = d['created_at']
    if 'data' in d:
      self.data = d['data']
    if 'id' in d:
      self.id = d['id']
    if 'label' in d:
      self.label = d['label']
    if 'node_id' in d:
      self.node_id = d['node_id']
    if 'scan_options' in d:
      self.scan_options = d['scan_options']
    if 'task_id' in d:
      self.task_id = d['task_id']
    if 'tsv' in d:
      self.tsv = d['tsv']
    if 'updated_at' in d:
      self.updated_at = d['updated_at']
  def to_dict(self):
    d = {}
    d['associated_id'] = self.associated_id
    d['category'] = self.category
    d['created_at'] = self.created_at
    d['data'] = self.data
    d['id'] = self.id
    d['label'] = self.label
    d['node_id'] = self.node_id
    d['scan_options'] = self.scan_options
    d['task_id'] = self.task_id
    d['tsv'] = self.tsv
    d['updated_at'] = self.updated_at
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def load(self):
    obj = self.http_get("/api/v2/node_scans/" + str(self.id) + ".json")
    self.from_dict(obj)
  

    
  def node(self):
    obj = self.http_get("/api/v2/nodes/{node_id}.json")
    elem = Node(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

