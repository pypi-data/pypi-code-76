# Copyright 2018 Xiaomi, Inc.
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

from . import models_util


class NamespaceService(object):
  """Class for namespace.
  """

  def __init__(self, name, owner_email, description):
    self.name = name
    self.owner_email = owner_email
    self.description = description

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, value):
    if not isinstance(value, str):
      raise ValueError("namespace name must be a string!")
    if value == "":
      raise ValueError("namespace name cannot be None!")
    if not models_util.check_kube_resource_name_regex(value):
      raise Exception("namespace name must match {}.".format(
          models_util.kube_resource_name_regex))
    self._name = value

  @property
  def owner_email(self):
    return self._owner_email

  @owner_email.setter
  def owner_email(self, value):
    if value and not isinstance(value, str):
      raise ValueError("owner_email must be a string!")
    # TODO(xychu): add email regex check
    self._owner_email = value

  @property
  def description(self):
    return self._description

  @description.setter
  def description(self, value):
    if value and not isinstance(value, str):
      raise ValueError("description must be a string!")
    self._description = value

  def get_json_data(self):
    data = {
      "name": self._name,
      "owner_email": self._owner_email,
      "description": self._description,
    }

    return json.dumps(data)
