import json
from .BaseObject import BaseObject
class SystemMetric(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.metric = None
    self.value = None
    self.timestamp = None
  def from_dict(self, d):
    if 'metric' in d:
      self.metric = d['metric']
    if 'value' in d:
      self.value = d['value']
    if 'timestamp' in d:
      self.timestamp = d['timestamp']
  def to_dict(self):
    d = {}
    d['metric'] = self.metric
    d['value'] = self.value
    d['timestamp'] = self.timestamp
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
