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


class NamespaceQuotaService(object):
  """Class for namespace quota.
  """

  def __init__(self, name, cpu, memory, gpu):
    self.name = name
    self.cpu = cpu
    self.memory = memory
    self.gpu = gpu

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
  def cpu(self):
    return self._cpu

  @cpu.setter
  def cpu(self, value):
    self._cpu = value

  @property
  def memory(self):
    return self._memory

  @memory.setter
  def memory(self, value):
    self._memory = value

  @property
  def gpu(self):
    return self._gpu

  @gpu.setter
  def gpu(self, value):
    self._gpu = value

  def get_json_data(self):
    data = {
      "name": self._name,
      "cpu": self._cpu,
      "memory": self._memory,
      "gpu": self._gpu,
    }

    return json.dumps(data)
