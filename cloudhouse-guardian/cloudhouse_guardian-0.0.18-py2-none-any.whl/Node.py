import json
from .BaseObject import BaseObject
from .NodeMediumInfo import NodeMediumInfo
from .NodeScanList import NodeScanList
from .NodeScan import NodeScan
class Node(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.connection_manager_group_id = None
    self.environment_id = None
    self.external_id = None
    self.id = None
    self.ip_address = None
    self.last_scan_status = None
    self.last_scan_status_string = None
    self.mac_address = None
    self.medium_hostname = None
    self.medium_info = NodeMediumInfo(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    self.medium_port = None
    self.medium_type = None
    self.medium_username = None
    self.name = None
    self.node_type = None
    self.online = None
    self.operating_system_family_id = None
    self.operating_system_id = None
    self.short_description = None
  def from_dict(self, d):
    if 'connection_manager_group_id' in d:
      self.connection_manager_group_id = d['connection_manager_group_id']
    if 'environment_id' in d:
      self.environment_id = d['environment_id']
    if 'external_id' in d:
      self.external_id = d['external_id']
    if 'id' in d:
      self.id = d['id']
    if 'ip_address' in d:
      self.ip_address = d['ip_address']
    if 'last_scan_status' in d:
      self.last_scan_status = d['last_scan_status']
    if 'last_scan_status_string' in d:
      self.last_scan_status_string = d['last_scan_status_string']
    if 'mac_address' in d:
      self.mac_address = d['mac_address']
    if 'medium_hostname' in d:
      self.medium_hostname = d['medium_hostname']
    if 'medium_info' in d:
      self.medium_info = d['medium_info']
    if 'medium_port' in d:
      self.medium_port = d['medium_port']
    if 'medium_type' in d:
      self.medium_type = d['medium_type']
    if 'medium_username' in d:
      self.medium_username = d['medium_username']
    if 'name' in d:
      self.name = d['name']
    if 'node_type' in d:
      self.node_type = d['node_type']
    if 'online' in d:
      self.online = d['online']
    if 'operating_system_family_id' in d:
      self.operating_system_family_id = d['operating_system_family_id']
    if 'operating_system_id' in d:
      self.operating_system_id = d['operating_system_id']
    if 'short_description' in d:
      self.short_description = d['short_description']
  def to_dict(self):
    d = {}
    d['connection_manager_group_id'] = self.connection_manager_group_id
    d['environment_id'] = self.environment_id
    d['external_id'] = self.external_id
    d['id'] = self.id
    d['ip_address'] = self.ip_address
    d['last_scan_status'] = self.last_scan_status
    d['last_scan_status_string'] = self.last_scan_status_string
    d['mac_address'] = self.mac_address
    d['medium_hostname'] = self.medium_hostname
    d['medium_info'] = self.medium_info.to_dict()
    d['medium_port'] = self.medium_port
    d['medium_type'] = self.medium_type
    d['medium_username'] = self.medium_username
    d['name'] = self.name
    d['node_type'] = self.node_type
    d['online'] = self.online
    d['operating_system_family_id'] = self.operating_system_family_id
    d['operating_system_id'] = self.operating_system_id
    d['short_description'] = self.short_description
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def load(self):
    obj = self.http_get("/api/v2/nodes/" + str(self.id) + ".json")
    self.from_dict(obj)
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      return self.update()
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/nodes.json", d)
    self.from_dict(out)
  

    
  def update(self):
    d = self.to_dict()
    if "id" in d:
      del d["id"]
    if "online" in d:
      del d["online"]
    if "last_scan_status" in d:
      del d["last_scan_status"]
    if "last_scan_status_string" in d:
      del d["last_scan_status_string"]
    self.http_put("/api/v2/nodes/" + str(self.id) + ".json", d)
  

    
  def delete(self):
    self.http_delete("/api/v2/nodes/" + str(self.id) + ".json")
  

    
  def connection_manager_group(self):
    obj = self.http_get("/api/v2/connection_manager_groups/{connection_manager_group_id}.json")
    elem = ConnectionManagerGroup(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

    
  def environment(self):
    obj = self.http_get("/api/v2/environments/" + str(self.environment_id) + ".json")
    elem = Environment(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

    
  def operating_system(self):
    obj = self.http_get("/api/v2/operating_systems/" + str(self.operating_system_id) + ".json")
    elem = OperatingSystem(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

    
  def operating_system_family(self):
    obj = self.http_get("/api/v2/operating_system_families/" + str(self.operating_system_family_id) + ".json")
    elem = OperatingSystemFamily(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

    
  def start_scan(self):
    url = "/api/v2/nodes/" + str(self.id) + "/start_scan.json"
    obj = self.http_post(url, None)
    return obj
  

    
  def node_scans(self):
    url = "/api/v2/node_scans.json?node_id=" + str(self.id) + "&per_page=5000"
    obj = self.http_get(url)
    the_list = NodeScanList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = NodeScan(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.node_id = x["node_id"]
      elem.created_at = x["created_at"]
      elem.updated_at = x["updated_at"]
      elem.scan_options = x["scan_options"]
      the_list.append(elem)
    return the_list
  

    
  def node_groups(self):
    obj = self.http_get("/api/v2/nodes/" + str(self.id) + "/node_groups.json")
    the_list = NodeGroupList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = NodeGroup(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      if "description" in x:
        elem.description = x["description"]
      if "node_rules" in x:
        elem.node_rules = x["node_rules"]
      the_list.append(elem)
    return the_list
  

    
  def raw_files(self):
    obj = self.http_get("/api/v2/nodes/" + str(self.id) + "/raw_files.json")
    the_list = RawFileList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = RawFile(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "node_scan_id" in x:
        elem.node_scan_id = x["node_scan_id"]
      if "created_at" in x:
        elem.created_at = x["created_at"]
      if "updated_at" in x:
        elem.updated_at = x["updated_at"]
      the_list.append(elem)
    return the_list
  

