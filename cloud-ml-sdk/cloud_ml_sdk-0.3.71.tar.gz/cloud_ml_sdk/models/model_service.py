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


class ModelService(object):
  """The model of model service.
  """

  def __init__(self,
               model_name,
               model_version,
               model_uri,
               model_args=None,
               fds_endpoint=None,
               fds_bucket=None,
               cpu_limit=None,
               gpu_limit=None,
               gpu_type=None,
               memory_limit=None,
               framework=None,
               framework_version=None,
               docker_image=None,
               docker_command=None,
               replicas=None,
               prepare_command=None,
               finish_command=None,
               node_selector_key=None,
               node_selector_value=None,
               enable_rank = None,
               debug = None,
               save_mode = False,
               use_seldon = False,
               engine_cpu = None,
               engine_mem = None,
               run_class_name = None,
               service_schema = None,
               initial_delay_sec = None,
               pod_replicas = None,
               use_http = None):
    self.model_name = model_name
    self.model_version = model_version
    self.model_uri = model_uri
    self.model_args = model_args
    self.fds_endpoint = fds_endpoint
    self.fds_bucket = fds_bucket
    self.cpu_limit = cpu_limit
    self.gpu_limit = gpu_limit
    self.gpu_type = gpu_type
    self.memory_limit = memory_limit
    self.framework = framework
    self.framework_version = framework_version
    self.docker_image = docker_image
    self.docker_command = docker_command
    self.replicas = replicas
    self.prepare_command = prepare_command
    self.finish_command = finish_command
    self.node_selector_key = node_selector_key
    self.node_selector_value = node_selector_value
    self.enable_rank = enable_rank
    self.debug = debug
    self.save_mode = save_mode
    self.use_seldon = use_seldon
    self.engine_cpu = engine_cpu
    self.engine_mem = engine_mem
    self.run_class_name = run_class_name
    self.service_schema = service_schema
    self.initial_delay_sec = initial_delay_sec
    self.pod_replicas = pod_replicas
    self.use_http = use_http

  @property
  def model_name(self):
    return self._model_name

  @model_name.setter
  def model_name(self, value):
    if not isinstance(value, str):
      raise ValueError("The type should be string")
    if not models_util.check_kube_resource_name_regex(value):
      raise Exception("model_name must match {}.".format(
          models_util.kube_resource_name_regex))
    self._model_name = value

  @property
  def model_version(self):
    return self._model_version

  @model_version.setter
  def model_version(self, value):
    if not isinstance(value, str):
      raise ValueError("The type should be string")
    self._model_version = value

  @property
  def model_uri(self):
    return self._model_uri

  @model_uri.setter
  def model_uri(self, value):
    if not isinstance(value, str):
      raise ValueError("The type should be string")
    self._model_uri = value

  @property
  def model_args(self):
    return self._model_args

  @model_args.setter
  def model_args(self, value):
    """Function for setting model_args.

    Args:
      value: The model arguments.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("model_args must be a string!")
    self._model_args = value

  @property
  def fds_endpoint(self):
    return self._fds_endpoint

  @fds_endpoint.setter
  def fds_endpoint(self, value):
    """Function for setting fds_endpoint.

    Args:
      value: The fds endpoint.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("fds_endpoint must be a string!")
    self._fds_endpoint = value

  @property
  def fds_bucket(self):
    return self._fds_bucket

  @fds_bucket.setter
  def fds_bucket(self, value):
    """Function for setting fds_bucket.

    Args:
      value: The fds bucket.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("fds_bucket must be a string!")
    self._fds_bucket = value

  @property
  def cpu_limit(self):
    return self._cpu_limit

  @cpu_limit.setter
  def cpu_limit(self, value):
    self._cpu_limit = models_util.check_cpu_value(value)

  @property
  def gpu_limit(self):
    return self._gpu_limit

  @gpu_limit.setter
  def gpu_limit(self, value):
    self._gpu_limit = models_util.check_gpu_value(value)

  @property
  def gpu_type(self):
    return self._gpu_type

  @gpu_type.setter
  def gpu_type(self, value):
    """Function for setting gpu_type.

    Args:
      value: GPU type

    Raises:
      ValueError: If value is not in constant.GPULIST
    """
    if value is not None:
      if constant.ENABLE_GPU_TYPE_SELECT:
        if (not (isinstance(value, str))) or (value.lower() not in constant.GPULIST):
          raise ValueError("Only support GPU types in ({})".format("/".join(constant.GPULIST)))
      else:
        raise ValueError("Select GPU type(gpu_type) is not supported, CloudML will try to find the best to use.\n" +
                         "If you have special reasons, please contact us.")
    self._gpu_type = value

  @property
  def memory_limit(self):
    return self._memory_limit

  @memory_limit.setter
  def memory_limit(self, value):
    self._memory_limit = models_util.check_memory_value(value)

  @property
  def framework(self):
    return self._framework

  @framework.setter
  def framework(self, value):
    """Function for setting framework.

    Args:
      value: The framework.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("Must be a string!")
    self._framework = value

  @property
  def framework_version(self):
    return self._framework_version

  @framework_version.setter
  def framework_version(self, value):
    """Function for setting version of framework.

    Args:
      value: The version of framework.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("Must be a string!")
    self._framework_version = value

  @property
  def docker_image(self):
    return self._docker_image

  @docker_image.setter
  def docker_image(self, value):
    """Function for setting docker_image.

    Args:
      value: The docker_image.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("Must be a string!")
    self._docker_image = value

  @property
  def docker_command(self):
    return self._docker_command

  @docker_command.setter
  def docker_command(self, value):
    """Function for setting docker_command.

    Args:
      value: The docker_command.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("Must be a string!")
    self._docker_command = value

  @property
  def replicas(self):
    return self._replicas

  @replicas.setter
  def replicas(self, value):
    """Function for setting replicas.

    Args:
      value: The replicas num.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not (isinstance(value, int) and value > 0):
        raise ValueError("replicas must be a postive integer!")
    self._replicas = value

  @property
  def prepare_command(self):
    return self._prepare_command

  @prepare_command.setter
  def prepare_command(self, value):
    """Function for set prepare_command.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not string instance or empty.
    """
    if value == "":
      raise ValueError("Prepare command can not be None!")
    self._prepare_command = value

  @property
  def finish_command(self):
    return self._finish_command

  @finish_command.setter
  def finish_command(self, value):
    """Function for set finish_command.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not string instance or empty.
    """
    if value == "":
      raise ValueError("Finish command can not be None!")
    self._finish_command = value

  @property
  def node_selector_key(self):
    return self._node_selector_key

  @node_selector_key.setter
  def node_selector_key(self, value):
    """Function for set node_selector_key.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not string instance or empty.
    """
    if value == "":
      raise ValueError("Node selector key can not be None!")
    self._node_selector_key = value

  @property
  def node_selector_value(self):
    return self._node_selector_value

  @node_selector_value.setter
  def node_selector_value(self, value):
    """Function for set node_selector_value.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not string instance or empty.
    """
    if value == "":
      raise ValueError("Node selector value can not be None!")
    self._node_selector_value = value

  @property
  def enable_rank(self):
    return self._enable_rank

  @enable_rank.setter
  def enable_rank(self, value):
    if value is None:
      self._enable_rank = 0
    else:
      self._enable_rank = value

  @property
  def debug(self):
    return self._debug
  @debug.setter
  def debug(self, value):
    if value is None:
      self._debug = 0
    else:
      self._debug = value

  @property
  def save_mode(self):
    return self._save_mode
  @save_mode.setter
  def save_mode(self, value):
    self._save_mode = value

  @property
  def use_seldon(self):
    return self._use_seldon
  @use_seldon.setter
  def use_seldon(self, value):
    if value and len(self._model_name) > 24:
      raise ("Cloudml model name should be up to maximum length of 24 characters and consist of lower case alphanumeric characters, - , and .")
    self._use_seldon = value

  @property
  def engine_cpu(self):
    return self._engine_cpu
  @engine_cpu.setter
  def engine_cpu(self,value):
    self._engine_cpu = value

  @property
  def engine_mem(self):
    return self._engine_mem
  @engine_mem.setter
  def engine_mem(self,value):
    self._engine_mem = value

  @property
  def run_class_name(self):
    return self._run_class_name
  @run_class_name.setter
  def run_class_name(self,value):
    self._run_class_name = value

  @property
  def service_schema(self):
    return self._service_schema
  @service_schema.setter
  def service_schema(self,value):
    if value is not None and value.upper() not in ["REST","GRPC"]:
      raise ("Service_schema must be GRPC or REST")
    if value is None:
      self._service_schema = ''
    else:
      self._service_schema = value.upper()

  @property
  def initial_delay_sec(self):
    return self._initial_delay_sec
  @initial_delay_sec.setter
  def initial_delay_sec(self, value):
    if value:
      if not value.isdigit():
        raise ValueError("initial_delay_sec value must be a number!")
      else:
        self._initial_delay_sec = value
    else:
      self._initial_delay_sec = None

  @property
  def pod_replicas(self):
    return self._pod_replicas
  @pod_replicas.setter
  def pod_replicas(self,value):
    if value:
      if not value.isdigit():
        raise ValueError("pod_replicas value must be a number!")
      else:
        self._pod_replicas = value
    else:
      self._pod_replicas = None

  @property
  def use_http(self):
    return self._use_http
  @use_http.setter
  def use_http(self,value):
    self._use_http = value

  def get_json_data(self):
    data = {
        "model_name": self._model_name,
        "model_version": self._model_version,
        "model_uri": self._model_uri,
        "enable_rank": self._enable_rank,
        "save_mode": self._save_mode
    }
    if self._fds_endpoint is not None:
      data["fds_endpoint"] = self._fds_endpoint
    if self._fds_bucket is not None:
      data["fds_bucket"] = self._fds_bucket
    if self._model_args:
      data["model_args"] = self._model_args
    if self._cpu_limit:
      data["cpu_limit"] = self._cpu_limit
    if self._gpu_limit:
      data["gpu_limit"] = self._gpu_limit
    if self._memory_limit:
      data["memory_limit"] = self._memory_limit
    if self._framework:
      data["framework"] = self._framework
    if self._framework_version:
      data["framework_version"] = self._framework_version
    if self._docker_image:
      data["docker_image"] = self._docker_image
    if self._docker_command:
      data["docker_command"] = self._docker_command
    if self._replicas:
      data["replicas"] = self._replicas
    if self._prepare_command:
      data["prepare_command"] = self._prepare_command
    if self._finish_command:
      data["finish_command"] = self._finish_command
    if self._node_selector_key:
      data["node_selector_key"] = self._node_selector_key
    if self._node_selector_value:
      data["node_selector_value"] = self._node_selector_value
    if self._gpu_type:
      data["gpu_type"] = self._gpu_type
    if self._debug:
      data["debug"] = self._debug
    if self._use_seldon:
      data["use_seldon"] = self._use_seldon
    if self._engine_cpu:
      data["engine_cpu"] = self._engine_cpu
    if self._engine_mem:
      data["engine_mem"] = self._engine_mem
    if self._run_class_name:
      data["run_class_name"] = self._run_class_name
    if self._service_schema:
      data["service_schema"] = self._service_schema
    if self._initial_delay_sec:
      data["initial_delay_sec"] = self._initial_delay_sec
    if self._pod_replicas:
      data["pod_replicas"] = self._pod_replicas
    if self._use_http:
      data["tensorflow_service_http"] = self._use_http
    return json.dumps(data)
