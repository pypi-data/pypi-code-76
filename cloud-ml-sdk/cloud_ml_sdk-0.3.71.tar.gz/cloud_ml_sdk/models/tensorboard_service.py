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
from . import constant
from . import models_util


class TensorboardService(object):
  """Class for tensorboard method.
  """

  def __init__(self,
               tensorboard_name,
               logdir,
               framework=None,
               framework_version=None,
               docker_image=None,
               docker_command=None,
               fds_endpoint=None,
               fds_bucket=None,
               node_selector_key=None,
               node_selector_value=None,
               enable_rank=None):
    self.tensorboard_name = tensorboard_name
    self.logdir = logdir
    self.framework = framework
    self.framework_version = framework_version
    self.docker_image = docker_image
    self.docker_command = docker_command
    self.fds_endpoint = fds_endpoint
    self.fds_bucket = fds_bucket
    self.node_selector_key = node_selector_key
    self.node_selector_value = node_selector_value
    self.enable_rank = enable_rank

  @property
  def tensorboard_name(self):
    return self._tensorboard_name

  @tensorboard_name.setter
  def tensorboard_name(self, value):
    if not isinstance(value, str):
      raise ValueError("tensorboard_name must be a string!")
    if value == "":
      raise ValueError("tensorboard_name cannot be None!")
    if not models_util.check_kube_resource_name_regex(value):
      raise Exception("tensorboard_name must match {}.".format(
          models_util.kube_resource_name_regex))
    self._tensorboard_name = value

  @property
  def logdir(self):
    return self._logdir

  @logdir.setter
  def logdir(self, value):
    if not isinstance(value, str):
      raise ValueError("logdir must be a string!")
    if value == "":
      raise ValueError("logdir cannot be None!")
    self._logdir = value

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

  def get_json_data(self):
    data = {
        "tensorboard_name": self._tensorboard_name,
        "logdir": self._logdir,
        "enable_rank": self._enable_rank,
    }
    if self._docker_image is not None:
      data["docker_image"] = self._docker_image
    if self._docker_command is not None:
      data["docker_command"] = self._docker_command
    if self._framework is not None:
      data["framework"] = self._framework
    if self._framework_version is not None:
      data["framework_version"] = self._framework_version
    if self._fds_endpoint is not None:
      data["fds_endpoint"] = self._fds_endpoint
    if self._fds_bucket is not None:
      data["fds_bucket"] = self._fds_bucket
    if self._node_selector_key:
      data["node_selector_key"] = self._node_selector_key
    if self._node_selector_value:
      data["node_selector_value"] = self._node_selector_value

    return json.dumps(data)
