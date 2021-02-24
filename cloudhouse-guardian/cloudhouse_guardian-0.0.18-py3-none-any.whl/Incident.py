import json
from .BaseObject import BaseObject
class Incident(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.ended_at = None
    self.external_id = None
    self.id = None
    self.short_description = None
    self.started_at = None
    self.url = None
  def from_dict(self, d):
    if 'ended_at' in d:
      self.ended_at = d['ended_at']
    if 'external_id' in d:
      self.external_id = d['external_id']
    if 'id' in d:
      self.id = d['id']
    if 'short_description' in d:
      self.short_description = d['short_description']
    if 'started_at' in d:
      self.started_at = d['started_at']
    if 'url' in d:
      self.url = d['url']
  def to_dict(self):
    d = {}
    d['ended_at'] = self.ended_at
    d['external_id'] = self.external_id
    d['id'] = self.id
    d['short_description'] = self.short_description
    d['started_at'] = self.started_at
    d['url'] = self.url
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
