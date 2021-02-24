import json
from .BaseObject import BaseObject
class ChangeRequest(BaseObject):
  def __init__(self, appliance_url, appliance_api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, appliance_api_key, sec_key, insecure)
    self.data = None
    self.ended_at = None
    self.external_id = None
    self.id = None
    self.planned_end_at = None
    self.planned_start_at = None
    self.short_description = None
    self.started_at = None
    self.url = None
  def from_dict(self, d):
    if 'data' in d:
      self.data = d['data']
    if 'ended_at' in d:
      self.ended_at = d['ended_at']
    if 'external_id' in d:
      self.external_id = d['external_id']
    if 'id' in d:
      self.id = d['id']
    if 'planned_end_at' in d:
      self.planned_end_at = d['planned_end_at']
    if 'planned_start_at' in d:
      self.planned_start_at = d['planned_start_at']
    if 'short_description' in d:
      self.short_description = d['short_description']
    if 'started_at' in d:
      self.started_at = d['started_at']
    if 'url' in d:
      self.url = d['url']
  def to_dict(self):
    d = {}
    d['data'] = self.data
    d['ended_at'] = self.ended_at
    d['external_id'] = self.external_id
    d['id'] = self.id
    d['planned_end_at'] = self.planned_end_at
    d['planned_start_at'] = self.planned_start_at
    d['short_description'] = self.short_description
    d['started_at'] = self.started_at
    d['url'] = self.url
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
