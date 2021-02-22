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


class NamespaceUserService(object):
  """Class for namespace user.
  """

  def __init__(self, namespace, user_id):
    self.namespace = namespace
    self.user_id = user_id

  @property
  def namespace(self):
    return self._namespace

  @namespace.setter
  def namespace(self, value):
    if not isinstance(value, str):
      raise ValueError("namespace name must be a string!")
    if value == "":
      raise ValueError("namespace name cannot be None!")
    if not models_util.check_kube_resource_name_regex(value):
      raise Exception("namespace name must match {}.".format(
          models_util.kube_resource_name_regex))
    self._namespace = value

  @property
  def user_id(self):
    return self._user_id

  @user_id.setter
  def user_id(self, value):
    if not isinstance(value, str):
      raise ValueError("user_id must be a str!")
    self._user_id = value

  def get_json_data(self):
    data = {
      "namespace": self._namespace,
      "user_id": self._user_id,
    }

    return json.dumps(data)
