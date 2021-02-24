import json
from .BaseObject import BaseObject
from .ConnectionManager import ConnectionManager
from .ConnectionManagerList import ConnectionManagerList
from .ConnectionManagerGroup import ConnectionManagerGroup
from .ConnectionManagerGroupList import ConnectionManagerGroupList
from .Environment import Environment
from .EnvironmentList import EnvironmentList
from .EventAction import EventAction
from .EventActionList import EventActionList
from .EventVariables import EventVariables
from .ExternalEvent import ExternalEvent
from .Incident import Incident
from .IncidentList import IncidentList
from .Job import Job
from .JobList import JobList
from .Node import Node
from .NodeList import NodeList
from .NodeGroup import NodeGroup
from .NodeGroupList import NodeGroupList
from .NodeGroupUser import NodeGroupUser
from .NodeGroupUserList import NodeGroupUserList
from .NodeMediumInfo import NodeMediumInfo
from .OperatingSystem import OperatingSystem
from .OperatingSystemList import OperatingSystemList
from .OperatingSystemFamily import OperatingSystemFamily
from .OperatingSystemFamilyList import OperatingSystemFamilyList
from .Pluggable import Pluggable
from .PluggableList import PluggableList
from .Policy import Policy
from .PolicyList import PolicyList
from .ScheduledJobList import ScheduledJobList
from .ScheduledJob import ScheduledJob
from .SystemMetric import SystemMetric
from .SystemMetricList import SystemMetricList
from .User import User
from .UserList import UserList
class Account(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.id = None
    self.name = None
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['id']
    if 'name' in d:
      self.name = d['name']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def change_request_by_id(self, id):
    obj = self.http_get("/api/v2/change_requests/" + str(id) + ".json")
    elem = ChangeRequest(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.external_id = obj["external_id"]
    elem.id = obj["id"]
    elem.planned_end_date = obj["planned_end_date"]
    elem.planned_start_date = obj["planned_start_date"]
    elem.short_description = obj["short_description"]
    elem.started_at = obj["started_at"]
    elem.ended_at = obj["ended_at"]
    return elem
  

    
  def change_requests(self):
    obj = self.http_get("/api/v2/change_requests.json")
    the_list = ChangeRequestList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = ChangeRequest(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "external_id" in x:
        elem.external_id = x["external_id"]
      if "id" in x:
        elem.id = x["id"]
      if "planned_end_date" in x:
        elem.planned_end_date = x["planned_end_date"]
      if "planned_start_date" in x:
        elem.planned_start_date = x["planned_start_date"]
      if "short_description" in x:
        elem.short_description = x["short_description"]
      if "started_at" in x:
        elem.started_at = x["started_at"]
      if "ended_at" in x:
        elem.ended_at = x["ended_at"]
      the_list.append(elem)
    return the_list
  

    
  def new_connection_manager_group(self):
    return ConnectionManagerGroup(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
  

    
  def connection_managers(self):
    obj = self.http_get("/api/v2/connection_managers.json")
    the_list = ConnectionManagerList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = ConnectionManager(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "agent_version" in x:
        elem.agent_version = x["agent_version"]
      if "agent_type" in x:
        elem.agent_type = x["agent_type"]
      if "channels" in x:
        elem.channels = x["channels"]
      if "connection_manager_group_id" in x:
        elem.connection_manager_group_id = x["connection_manager_group_id"]
      if "created_at" in x:
        elem.created_at = x["created_at"]
      if "hostname" in x:
        elem.hostname = x["hostname"]
      if "id" in x:
        elem.id = x["id"]
      if "ip_address" in x:
        elem.ip_address = x["ip_address"]
      if "last_contact" in x:
        elem.last_contact = x["last_contact"]
      if "stats" in x:
        elem.stats = x["stats"]
      if "updated_at" in x:
        elem.updated_at = x["updated_at"]
      the_list.append(elem)
    return the_list
  

    
  def connection_manager_groups(self):
    obj = self.http_get("/api/v2/connection_manager_groups.json")
    the_list = ConnectionManagerGroupList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = ConnectionManagerGroup(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      if "api_key" in x:
        elem.api_key = x["api_key"]
      if "status" in x:
        elem.status = x["status"]
      the_list.append(elem)
    return the_list
  

    
  def new_environment(self):
    return Environment(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
  

    
  def environment_by_id(self, id):
    obj = self.http_get("/api/v2/environments/" + str(id) + ".json")
    elem = Environment(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

    
  def environment_by_name(self, name):
    url = "/api/v2/environments/lookup.json?name=" + str(name) + ""
    obj = self.http_get(url)
    id = obj["environment_id"]
    elem = Environment(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = id
    elem.load()
    return elem
  

    
  def environments(self):
    obj = self.http_get("/api/v2/environments.json")
    the_list = EnvironmentList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = Environment(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "description" in x:
        elem.description = x["description"]
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      if "node_rules" in x:
        elem.node_rules = x["node_rules"]
      if "short_description" in x:
        elem.short_description = x["short_description"]
      the_list.append(elem)
    return the_list
  

    
  def new_external_event(self):
    return ExternalEvent(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
  

    
  def events_with_view_name(self, view_name):
    url = "/api/v2/events.json?view_name=" + str(view_name) + ""
    obj = self.http_get(url)
    the_list = EventList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = Event(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.type_id = x["type_id"]
      elem.environment_id = x["environment_id"]
      elem.created_at = x["created_at"]
      the_list.append(elem)
    return the_list
  

    
  def events_with_query(self, query):
    url = "/api/v2/events.json?query=" + str(query) + ""
    obj = self.http_get(url)
    the_list = EventList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = Event(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      elem.id = x["id"]
      elem.type_id = x["type_id"]
      elem.environment_id = x["environment_id"]
      elem.created_at = x["created_at"]
      the_list.append(elem)
    return the_list
  

    
  def event_action_by_id(self, id):
    obj = self.http_get("/api/v2/event_actions/" + str(id) + ".json")
    elem = EventAction(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

    
  def event_types(self):
    obj = self.http_get("/api/v2/events/types.json")
    the_list = EventTypeList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = EventType(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      the_list.append(elem)
    return the_list
  

    
  def event_actions(self):
    obj = self.http_get("/api/v2/event_actions.json")
    the_list = EventActionList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = EventAction(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      if "status" in x:
        elem.status = x["status"]
      if "type" in x:
        elem.type = x["type"]
      if "variables" in x:
        elem.variables = x["variables"]
      if "view" in x:
        elem.view = x["view"]
      the_list.append(elem)
    return the_list
  

    
  def incidents(self):
    obj = self.http_get("/api/v2/incidents.json")
    the_list = IncidentList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = Incident(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "external_id" in x:
        elem.external_id = x["external_id"]
      if "short_description" in x:
        elem.short_description = x["short_description"]
      if "started_at" in x:
        elem.started_at = x["started_at"]
      if "ended_at" in x:
        elem.ended_at = x["ended_at"]
      if "url" in x:
        elem.url = x["url"]
      the_list.append(elem)
    return the_list
  

    
  def incident_by_id(self, id):
    obj = self.http_get("/api/v2/incidents/" + str(id) + ".json")
    elem = Incident(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.external_id = obj["external_id"]
    elem.short_description = obj["short_description"]
    elem.started_at = obj["started_at"]
    elem.ended_at = obj["ended_at"]
    elem.url = obj["url"]
    return elem
  

    
  def jobs(self):
    obj = self.http_get("/api/v2/jobs.json")
    the_list = JobList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = Job(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "source_id" in x:
        elem.source_id = x["source_id"]
      if "source_name" in x:
        elem.source_name = x["source_name"]
      if "source_type" in x:
        elem.source_type = x["source_type"]
      if "status" in x:
        elem.status = x["status"]
      the_list.append(elem)
    return the_list
  

    
  def job_by_id(self, id):
    obj = self.http_get("/api/v2/jobs/" + str(id) + ".json")
    elem = Job(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.source_id = obj["source_id"]
    elem.source_name = obj["source_name"]
    elem.source_type = obj["source_type"]
    elem.status = obj["status"]
    return elem
  

    
  def new_node(self):
    return Node(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
  

    
  def nodes(self):
    obj = self.http_get("/api/v2/nodes.json")
    the_list = NodeList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = Node(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "connection_manager_group_id" in x:
        elem.connection_manager_group_id = x["connection_manager_group_id"]
      if "external_id" in x:
        elem.external_id = x["external_id"]
      if "environment_id" in x:
        elem.environment_id = x["environment_id"]
      if "id" in x:
        elem.id = x["id"]
      if "ip_address" in x:
        elem.ip_address = x["ip_address"]
      if "last_scan_status" in x:
        elem.last_scan_status = x["last_scan_status"]
      if "last_scan_status_string" in x:
        elem.last_scan_status_string = x["last_scan_status_string"]
      if "mac_address" in x:
        elem.mac_address = x["mac_address"]
      if "medium_hostname" in x:
        elem.medium_hostname = x["medium_hostname"]
      if "medium_port" in x:
        elem.medium_port = x["medium_port"]
      if "medium_type" in x:
        elem.medium_type = x["medium_type"]
      if "medium_username" in x:
        elem.medium_username = x["medium_username"]
      if "name" in x:
        elem.name = x["name"]
      if "node_type" in x:
        elem.node_type = x["node_type"]
      if "online" in x:
        elem.online = x["online"]
      if "operating_system_family_id" in x:
        elem.operating_system_family_id = x["operating_system_family_id"]
      if "operating_system_id" in x:
        elem.operating_system_id = x["operating_system_id"]
      if "short_description" in x:
        elem.short_description = x["short_description"]
      if "medium_info" in x:
        elem.medium_info.from_dict(x["medium_info"])
      the_list.append(elem)
    return the_list
  

    
  def node_by_external_id(self, external_id):
    url = "/api/v2/nodes/lookup.json?external_id=" + str(external_id) + ""
    obj = self.http_get(url)
    id = obj["node_id"]
    elem = Node(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = id
    elem.load()
    return elem
  

    
  def node_by_name(self, name):
    url = "/api/v2/nodes/lookup.json?name=" + str(name) + ""
    obj = self.http_get(url)
    id = obj["node_id"]
    elem = Node(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = id
    elem.load()
    return elem
  

    
  def node_by_id(self, id):
    obj = self.http_get("/api/v2/nodes/" + str(id) + ".json")
    elem = Node(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

    
  def new_node_group(self):
    return NodeGroup(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
  

    
  def node_groups(self):
    obj = self.http_get("/api/v2/node_groups.json")
    the_list = NodeGroupList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = NodeGroup(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "description" in x:
        elem.description = x["description"]
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      if "node_rules" in x:
        elem.node_rules = x["node_rules"]
      if "search_query" in x:
        elem.search_query = x["search_query"]
      the_list.append(elem)
    return the_list
  

    
  def node_group_by_id(self, id):
    obj = self.http_get("/api/v2/node_groups/" + str(id) + ".json")
    elem = NodeGroup(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.name = obj["name"]
    return elem
  

    
  def node_group_by_name(self, name):
    url = "/api/v2/node_groups/lookup.json?name=" + str(name) + ""
    obj = self.http_get(url)
    id = obj["node_group_id"]
    elem = NodeGroup(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = id
    elem.load()
    return elem
  

    
  def node_scan_by_id(self, id):
    obj = self.http_get("/api/v2/node_scans/" + str(id) + ".json")
    elem = NodeScan(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.id = obj["id"]
    elem.node_id = obj["node_id"]
    elem.data = obj["data"]
    elem.scan_options = obj["scan_options"]
    elem.created_at = obj["created_at"]
    elem.updated_at = obj["updated_at"]
    elem.task_id = obj["task_id"]
    elem.associated_id = obj["associated_id"]
    elem.category = obj["category"]
    elem.label = obj["label"]
    elem.tsv = obj["tsv"]
    return elem
  

    
  def operating_system_families(self):
    obj = self.http_get("/api/v2/operating_system_families.json")
    the_list = OperatingSystemFamilyList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = OperatingSystemFamily(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      the_list.append(elem)
    return the_list
  

    
  def operating_systems(self):
    obj = self.http_get("/api/v2/operating_systems.json")
    the_list = OperatingSystemList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = OperatingSystem(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      if "operating_system_family_id" in x:
        elem.operating_system_family_id = x["operating_system_family_id"]
      if "description" in x:
        elem.description = x["description"]
      the_list.append(elem)
    return the_list
  

    
  def new_pluggable(self):
    return Pluggable(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
  

    
  def pluggables(self):
    obj = self.http_get("/api/v2/pluggables.json")
    the_list = PluggableList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = Pluggable(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "description" in x:
        elem.description = x["description"]
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      if "operating_system_family" in x:
        elem.operating_system_family = x["operating_system_family"]
      if "operating_system_family_id" in x:
        elem.operating_system_family_id = x["operating_system_family_id"]
      if "script" in x:
        elem.script = x["script"]
      the_list.append(elem)
    return the_list
  

    
  def new_policy(self):
    return Policy(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
  

    
  def policies(self):
    obj = self.http_get("/api/v2/policies.json")
    the_list = PolicyList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = Policy(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "description" in x:
        elem.description = x["description"]
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      if "short_description" in x:
        elem.short_description = x["short_description"]
      the_list.append(elem)
    return the_list
  

    
  def scheduled_jobs(self):
    obj = self.http_get("/api/v2/scheduled_jobs.json")
    the_list = ScheduledJobList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = ScheduledJob(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "data" in x:
        elem.data = x["data"]
      if "id" in x:
        elem.id = x["id"]
      if "source_id" in x:
        elem.source_id = x["source_id"]
      if "source_name" in x:
        elem.source_name = x["source_name"]
      if "source_type" in x:
        elem.source_type = x["source_type"]
      if "status" in x:
        elem.status = x["status"]
      the_list.append(elem)
    return the_list
  

    
  def system_metrics(self):
    obj = self.http_get("/api/v2/system_metrics.json")
    the_list = SystemMetricList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = SystemMetric(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "metric" in x:
        elem.metric = x["metric"]
      if "value" in x:
        elem.value = x["value"]
      if "timestamp" in x:
        elem.timestamp = x["timestamp"]
      the_list.append(elem)
    return the_list
  

    
  def text_file_by_id(self, id):
    obj = self.http_get("/api/v2/text_files/" + str(id) + ".json")
    elem = TextFile(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    elem.category = obj["category"]
    elem.checksum = obj["checksum"]
    elem.created_at = obj["created_at"]
    elem.data = obj["data"]
    elem.id = obj["id"]
    elem.name = obj["name"]
    elem.updated_at = obj["updated_at"]
    return elem
  

    
  def users(self):
    obj = self.http_get("/api/v2/users.json")
    the_list = UserList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = User(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "email" in x:
        elem.email = x["email"]
      if "id" in x:
        elem.id = x["id"]
      if "last_sign_in_at" in x:
        elem.last_sign_in_at = x["last_sign_in_at"]
      if "name" in x:
        elem.name = x["name"]
      if "role" in x:
        elem.role = x["role"]
      if "surname" in x:
        elem.surname = x["surname"]
      if "external_id" in x:
        elem.external_id = x["external_id"]
      the_list.append(elem)
    return the_list
  

    
  def users_and_invitees(self):
    obj = self.http_get("/api/v2/users.json?invited=true")
    the_list = UserList(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = User(self.appliance_url, self.appliance_api_key, self.sec_key, self.insecure)
      if "email" in x:
        elem.email = x["email"]
      if "expiry" in x:
        elem.expiry = x["expiry"]
      if "id" in x:
        elem.id = x["id"]
      if "invited" in x:
        elem.invited = x["invited"]
      if "last_sign_in_at" in x:
        elem.last_sign_in_at = x["last_sign_in_at"]
      if "name" in x:
        elem.name = x["name"]
      if "role" in x:
        elem.role = x["role"]
      if "surname" in x:
        elem.surname = x["surname"]
      if "external_id" in x:
        elem.external_id = x["external_id"]
      the_list.append(elem)
    return the_list
  

    
  def invite_user(self, email, role):
    url = "/api/v2/users/invite.json?email=" + str(email) + "&role=" + str(role) + ""
    obj = self.http_post(url, None)
    return obj
  

    
  def remove_user(self, email):
    url = "/api/v2/users/remove.json?email=" + str(email) + ""
    obj = self.http_put(url, None)
    return obj

