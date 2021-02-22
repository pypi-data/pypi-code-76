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


class DevEnv(object):
  """The model of dev environment.
  """

  def __init__(self,
               dev_name,
               password,
               fds_endpoint=None,
               fds_bucket=None,
               hdfs_krb_account=None,
               hdfs_krb_password=None,
               hdfs_endpoint=None,
               hdfs_krb_keytab=None,
               ceph_volume=None,
               ceph_mode=None,
               cpu_limit=None,
               gpu_limit=None,
               gpu_type=None,
               memory_limit=None,
               framework=None,
               framework_version=None,
               docker_image=None,
               docker_command=None,
               node_selector_key=None,
               node_selector_value=None,
               network=None,
               enable_rank=None):
    self.dev_name = dev_name
    self.password = password
    self.fds_endpoint = fds_endpoint
    self.fds_bucket = fds_bucket
    self.hdfs_krb_account = hdfs_krb_account
    self.hdfs_krb_password = hdfs_krb_password
    self.hdfs_endpoint = hdfs_endpoint
    self.hdfs_krb_keytab = hdfs_krb_keytab
    self.ceph_volume = ceph_volume
    self.ceph_mode = ceph_mode
    self.cpu_limit = cpu_limit
    self.gpu_limit = gpu_limit
    self.gpu_type = gpu_type
    self.memory_limit = memory_limit
    self.framework = framework
    self.framework_version = framework_version
    self.docker_image = docker_image
    self.docker_command = docker_command
    self.node_selector_key = node_selector_key
    self.node_selector_value = node_selector_value
    self.network = network
    self.enable_rank = enable_rank

  @property
  def dev_name(self):
    return self._dev_name

  @dev_name.setter
  def dev_name(self, value):
    if not isinstance(value, str):
      raise ValueError("The type should be string")
    if not models_util.check_kube_resource_name_regex(value):
      raise Exception("dev_name must match {}.".format(
          models_util.kube_resource_name_regex))
    self._dev_name = value

  @property
  def password(self):
    return self._password

  @password.setter
  def password(self, value):
    if not isinstance(value, str):
      raise ValueError("The type should be string")
    self._password = value

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
  def hdfs_krb_account(self):
    return self._hdfs_krb_account

  @hdfs_krb_account.setter
  def hdfs_krb_account(self, value):
    if value != None:
      if not isinstance(value, str):
        raise ValueError("hdfs_krb_account must be a string!")
    self._hdfs_krb_account = value

  @property
  def hdfs_krb_password(self):
    return self._hdfs_krb_password

  @hdfs_krb_password.setter
  def hdfs_krb_password(self, value):
    if value != None:
      if not isinstance(value,str):
        raise ValueError("hdfs_krb_password must be a string!")
    self._hdfs_krb_password = value

  @property
  def hdfs_endpoint(self):
    return self._hdfs_endpoint

  @hdfs_endpoint.setter
  def hdfs_endpoint(self, value):
    if value != None:
      if not isinstance(value,str) or not value.startswith("hdfs://"):
        raise ValueError("hdfs_endpoint must start with hdfs://")
    self._hdfs_endpoint = value

  @property
  def hdfs_krb_keytab(self):
    return self._hdfs_krb_keytab

  @hdfs_krb_keytab.setter
  def hdfs_krb_keytab(self, value):
    if value != None:
      if not isinstance(value, str):
        raise ValueError("hdfs_krb_keytab must be a string!")
    self._hdfs_krb_keytab = value

  @property
  def ceph_volume(self):
    return self._ceph_volume

  @hdfs_endpoint.setter
  def ceph_volume(self, value):
    if value != None:
      if not isinstance(value,str):
        raise ValueError("ceph_volume must be string")
    self._ceph_volume = value

  @property
  def ceph_mode(self):
    return self._ceph_mode

  @hdfs_endpoint.setter
  def ceph_mode(self, value):
    if value != None:
      if not isinstance(value,str) or not (value == "r" or value == "rw"):
        raise ValueError("ceph_mode must be r or rw")
    self._ceph_mode = value

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
  def network(self):
    return self._network

  @network.setter
  def network(self, value):
    if value is not None:
      if not isinstance(value,list):
        raise ("The network must be a list")
      jupyter_num = 0
      for i in value:
        if i["protocol"] not in list(constant.DEV_PROXY_PROTOCOL.values()):
          raise ("Network protocol must be in {}".format(str(constant.DEV_PROXY_PROTOCOL.values())))
        if i["protocol"] == "JUPYTER":
          jupyter_num += 1
        if jupyter_num > 1:
          raise ("Multiple JUPYTER protocol is not allowed")
        models_util.check_network_port(i["port"])
        for ip in i["whitelist"]:
          if not models_util.check_cidr(ip):
            raise ValueError("Network whitelist should be in CIDR format")
    self._network = value

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
    data = {"dev_name": self._dev_name,
            "password": self._password,
            "enable_rank": self._enable_rank}
    if self._fds_endpoint is not None:
      data["fds_endpoint"] = self._fds_endpoint
    if self._fds_bucket is not None:
      data["fds_bucket"] = self._fds_bucket
    if self._hdfs_krb_account is not None and  self._hdfs_endpoint is not None:
      data["hdfs_endpoint"] = self._hdfs_endpoint
      data["hdfs_krb_account"] = self._hdfs_krb_account
      if self._hdfs_krb_password is not None:
        data["hdfs_krb_password"] = self._hdfs_krb_password
      if self._hdfs_krb_keytab is not None:
        data["hdfs_krb_keytab"] = self._hdfs_krb_keytab
    if self._ceph_volume is not None and self._ceph_mode is not None:
      data["ceph_volume"] = self._ceph_volume
      data["ceph_mode"] = self._ceph_mode
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
    if self._node_selector_key:
      data["node_selector_key"] = self._node_selector_key
    if self._node_selector_value:
      data["node_selector_value"] = self._node_selector_value
    if self._gpu_type:
      data["gpu_type"] = self._gpu_type
    if self._network:
      data["network"] = self._network
    return json.dumps(data)
