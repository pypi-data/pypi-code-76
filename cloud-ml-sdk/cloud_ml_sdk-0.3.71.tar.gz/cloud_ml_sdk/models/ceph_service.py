# Copyright 2017 Xiaomi, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import re
from . import constant
from . import models_util

ceph_name_regex_pattern = re.compile("^[A-Za-z0-9]{2,10}$")
ceph_capacity_regex_pattern = re.compile("^[1-9][0-9]*[TGMtgm]$")

class CephService(object):
  """Class for ceph service method.
  """

  def __init__(self,
               ceph_name,
               capacity):
    self.ceph_name = ceph_name
    self.capacity = capacity


  @property
  def ceph_name(self):
    return self._ceph_name


  @ceph_name.setter
  def ceph_name(self, value):
    if not isinstance(value, str):
      raise ValueError("ceph_name must be a string!")
    if value == "":
      raise ValueError("ceph_name cannot be None!")
    if not ceph_name_regex_pattern.match(value):
      raise ValueError("ceph name must be an alphanumeric string of up to 10 characters")
    self._ceph_name = value


  @property
  def capacity(self):
    return self._capacity


  @capacity.setter
  def capacity(self, value):
    if not isinstance(value, str):
      raise ValueError("capacity must be a string!")
    if value == "":
      raise ValueError("capacity cannot be None!")
    if not ceph_capacity_regex_pattern.match(value):
      raise ValueError("ceph capacity must be string, e.g. 2M, 3G, 4T")
    self._capacity = value


  def get_json_data(self):
    data = {
        "ceph_name": self._ceph_name,
        "capacity": self._capacity
    }
    return json.dumps(data)
