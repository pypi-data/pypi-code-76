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
from ..command import constant
from . import models_util


class SecretService(object):
  """Class for secret method.
  """

  def __init__(self, secret_name, data):
    self.secret_name = secret_name
    self.data = data

  @property
  def secret_name(self):
    return self._secret_name

  @secret_name.setter
  def secret_name(self, value):
    if not isinstance(value, str):
      raise ValueError("secret_name must be a string!")
    if value == "":
      raise ValueError("secret_name cannot be None!")
    if not models_util.check_kube_resource_name_regex(value):
      raise Exception("secret_name must match {}.".format(
          models_util.kube_resource_name_regex))
    self._secret_name = value

  @property
  def data(self):
    return self._data

  @data.setter
  def data(self, value):
    if not isinstance(value, str):
      raise ValueError("data must be a string!")
    if value == "":
      raise ValueError("data cannot be Empty!")
    self._data = value

  def get_json_data(self):
    data = {
        "secret_name": self._secret_name,
        "data": self._data,
    }

    return json.dumps(data)
