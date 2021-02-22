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
import os
from datetime import datetime
import time

from ..command import constant
from . import models_util
from fds import GalaxyFDSClient
from cloud_ml_sdk.client import CloudMlClient


class TrainJob(object):
  """Class for train method.

  A TrainJob instance provides variables getter and setter apis. After
  specifying the necessary parameters, users can call start_run func to start
  the train job.
  """

  def __init__(self,
               job_name,
               module_name,
               trainer_uri,
               model_input_path=None,
               model_export_path=None,
               data_input_path=None,
               data_output_path=None,
               log_path=None,
               job_args=None,
               fds_endpoint=None,
               fds_bucket=None,
               hdfs_krb_account=None,
               hdfs_krb_password=None,
               hdfs_endpoint=None,
               cpu_limit=None,
               gpu_limit=None,
               gpu_type=None,
               memory_limit=None,
               framework=None,
               framework_version=None,
               docker_image=None,
               docker_command=None,
               volume_type=None,
               volume_path=None,
               mount_path=None,
               mount_read_only=None,
               prepare_command=None,
               finish_command=None,
               node_selector_key=None,
               node_selector_value=None,
               ps_count=None,
               worker_count=None,
               cluster_spec=None,
               enable_rank=None,
               pipeline_id=None,
               save_mode=False,
               tensorboard_logdir=None,
               model_name=None,
               model_version=None,
               hdfs_krb_keytab=None):
    """Creates a new TrainJob with given definition.

    The `job_name`, `module_name` and `trainer_uri` arguments must be provided
    when the object is creating.

    Args:
      job_name: The name of specific job.
      module_name: The name of module.
      trainer_uri: The uri that save the source code of job.
    """
    self.job_name = job_name
    self.module_name = module_name
    self.trainer_uri = trainer_uri

    self.model_input_path = model_input_path
    self.model_export_path = model_export_path
    self.data_input_path = data_input_path
    self.data_output_path = data_output_path
    self.log_path = log_path
    self.job_args = job_args
    self.fds_endpoint = fds_endpoint
    self.fds_bucket = fds_bucket
    self.hdfs_krb_account = hdfs_krb_account
    self.hdfs_krb_password = hdfs_krb_password
    self.hdfs_krb_keytab = hdfs_krb_keytab
    self.hdfs_endpoint = hdfs_endpoint
    self.cpu_limit = cpu_limit
    self.memory_limit = memory_limit
    self.gpu_limit = gpu_limit
    self.gpu_type = gpu_type
    self.framework = framework
    self.framework_version = framework_version
    self.docker_image = docker_image
    self.docker_command = docker_command
    self.volume_type = volume_type
    self.volume_path = volume_path
    self.mount_path = mount_path
    self.mount_read_only = mount_read_only
    self.prepare_command = prepare_command
    self.finish_command = finish_command
    self.node_selector_key = node_selector_key
    self.node_selector_value = node_selector_value
    self.cluster_spec = cluster_spec
    self.ps_count = ps_count
    self.worker_count = worker_count
    self.enable_rank = enable_rank
    self.pipeline_id = pipeline_id
    self.save_mode = save_mode
    self.tensorboard_logdir = tensorboard_logdir
    self.model_name = model_name
    self.model_version = model_version


  @property
  def job_name(self):
    return self._job_name

  @job_name.setter
  def job_name(self, value):
    """Function for setting job_name.

    Args:
      value: String type value that is going to be set to job_name. Which
             cannot be empty.

    Raises:
      ValueError: If value is not str instance or empty.
    """
    if not isinstance(value, str):
      raise ValueError("job_name must be a string!")
    if value == "":
      raise ValueError("job_name cannot be None!")
    if not models_util.check_kube_resource_name_regex(value):
      raise Exception("job_name must match {}.".format(
          models_util.kube_resource_name_regex))
    self._job_name = value

  @property
  def module_name(self):
    return self._module_name

  @module_name.setter
  def module_name(self, value):
    """Function for setting module_name.

    Args:
      value: String type value that is going to be set to module_name. Which
             cannot be empty.

    Raises:
      ValueError: If value is not str instance or empty.
    """
    if not isinstance(value, str):
      raise ValueError("module_name must be a string!")
    if value == "":
      raise ValueError("module_name cannot be None!")
    self._module_name = value

  @property
  def trainer_uri(self):
    return self._trainer_uri

  @trainer_uri.setter
  def trainer_uri(self, value):
    """Function for setting trainer_uri.

    Args:
      value: String type value that is going to be set to trainer_uri. Which
             cannot be empty. trainer_uri must be a valid local tar.gz file path
             or a valid fds tar.gz path

    Raises:
      ValueError: If value is in one of he following cases: not a str instance;
                  not a valid fds path; not a valid local path or file not exist.
    """

    self._trainer_uri = models_util.validate_and_get_trainer_uri(value)

  @property
  def job_args(self):
    return self._job_args

  @job_args.setter
  def job_args(self, value):
    """Function for setting job_args.

    Args:
      value: The job arguments.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("job_args must be a string!")
    self._job_args = value

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
      if not isinstance(value, str):
        raise ValueError("hdfs_krb_password must be a string!")
    self._hdfs_krb_password = value

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
  def hdfs_endpoint(self):
    return self._hdfs_endpoint

  @hdfs_endpoint.setter
  def hdfs_endpoint(self, value):
    if value != None:
      if not isinstance(value, str) or not value.startswith("hdfs://"):
        raise ValueError("hdfs_endpoint must start with hdfs://")
    self._hdfs_endpoint = value

  @property
  def cpu_limit(self):
    return self._cpu_limit

  @cpu_limit.setter
  def cpu_limit(self, value):
    """Function for setting cpu_limit.

    Args:
      value: Cpu limit.

    Raises:
      ValueError: If value is not a positive number.
    """
    self._cpu_limit = models_util.check_cpu_value(value)

  @property
  def memory_limit(self):
    return self._memory_limit

  @memory_limit.setter
  def memory_limit(self, value):
    """Function for setting memory_limit.

    Args:
      value: Memory limit.

    Raises:
      ValueError: Doesn't end with K, M or G.
    """
    self._memory_limit = models_util.check_memory_value(value)

  @property
  def gpu_limit(self):
    return self._gpu_limit

  @gpu_limit.setter
  def gpu_limit(self, value):
    """Function for setting gpu_limit.

    Args:
      value: GPU limit.

    Raises:
      ValueError: If value is not a positive number.
    """
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
  def model_input_path(self):
    return self._model_input_path

  @model_input_path.setter
  def model_input_path(self, value):
    self._model_input_path = value

  @property
  def model_export_path(self):
    return self._model_export_path

  @model_export_path.setter
  def model_export_path(self, value):
    self._model_export_path = value

  @property
  def data_input_path(self):
    return self._data_input_path

  @data_input_path.setter
  def data_input_path(self, value):
    self._data_input_path = value

  @property
  def data_output_path(self):
    return self._data_output_path

  @data_output_path.setter
  def data_output_path(self, value):
    self._data_output_path = value

  @property
  def log_path(self):
    return self._log_path

  @log_path.setter
  def log_path(self, value):
    self._log_path = value

  @property
  def pipeline_id(self):
    return self._pipeline_id

  @pipeline_id.setter
  def pipeline_id(self, value):
    self._pipeline_id = value

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
  def ps_count(self):
    return self._ps_count

  @ps_count.setter
  def ps_count(self, value):
    """Function for setting ps_count.

    Args:
      value: TensorFlow PS count.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value > 0):
        raise ValueError("ps_count must be a positive integer!")
    self._ps_count = value

  @property
  def worker_count(self):
    return self._worker_count

  @worker_count.setter
  def worker_count(self, value):
    """Function for setting worker_count.

    Args:
      value: TensorFlow worker count.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value > 0):
        raise ValueError("worker_count must be a positive integer!")
    self._worker_count = value

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
  def volume_type(self):
    return self._volume_type

  @volume_type.setter
  def volume_type(self, value):
    """Function for set.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not str instance or empty.
    """
    if value == "":
      raise ValueError("Volume type can not be None!")
    self._volume_type = value

  @property
  def volume_path(self):
    return self._volume_path

  @volume_path.setter
  def volume_path(self, value):
    """Function for set.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not str instance or empty.
    """
    if value == "":
      raise ValueError("Volume path can not be None!")
    self._volume_path = value

  @property
  def mount_path(self):
    return self._mount_path

  @mount_path.setter
  def mount_path(self, value):
    """Function for set.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not str instance or empty.
    """
    if value == "":
      raise ValueError("Mount path can not be None!")
    self._mount_path = value

  @property
  def mount_read_only(self):
    return self._mount_read_only

  @mount_read_only.setter
  def mount_read_only(self, value):
    """Function for set.

    Args:
      value: Boolean value.

    Raises:
      ValueError: If value is not boolean instance or empty.
    """
    if value != None and type(value) != bool:
      raise ValueError("Mount read only should be boolean!")
    self._mount_read_only = value

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
  def cluster_spec(self):
    return self._cluster_spec

  @cluster_spec.setter
  def cluster_spec(self, value):
    """Function for set distributed para.

    Args:
      value: Json value.

    Raises:
      ValueError: If value is in wrong format.
    """
    if value != None:
      if not isinstance(value, dict):
        raise ValueError("The cluster_spec must be a dict!")
      else:
        try:
          for task_type in value:
            task_msg = value[task_type]
            count = models_util.check_distributed_count(task_msg['count'])
            cpu_limit = models_util.check_cpu_value(task_msg['cpu_limit'])
            memory_limit = models_util.check_memory_value(task_msg['memory_limit'])
            gpu_limit = models_util.check_gpu_value(task_msg['gpu_limit'])
        except Exception as e:
          raise ValueError("Format error in cluster_spec dict, exception: {}".format(e))
    self._cluster_spec = value

  @property
  def save_mode(self):
    return self._save_mode

  @save_mode.setter
  def save_mode(self, value):
    self._save_mode = value

  @property
  def tensorboard_logdir(self):
    return self._tensorboard_logdir

  @tensorboard_logdir.setter
  def tensorboard_logdir(self, value):
    self._tensorboard_logdir= value

  @property
  def model_name(self):
    return self._model_name

  @model_name.setter
  def model_name(self, value):
    self._model_name = value

  @property
  def model_version(self):
    return self._model_version

  @model_version.setter
  def model_version(self, value):
    self._model_version = value


  def get_json_data(self):
    """Get the needed train job data after setting necessary varibles.

    Returns:
      data: The json data which is necessary for the train job.

    Raises:
      ValueError: If endpoint is not a string starting with `http://`.
                  If _job_name, _module_name or _trainer_uri is empty.
    """
    data = {
        "job_name": self._job_name,
        "module_name": self._module_name,
        "trainer_uri": self._trainer_uri,
        "enable_rank": self._enable_rank,
        "save_mode": self._save_mode
    }
    if self._model_input_path is not None:
      data["model_input_path"] = self._model_input_path
    if self._model_export_path is not None:
      data["model_export_path"] = self._model_export_path
    if self._data_input_path is not None:
      data["data_input_path"] = self._data_input_path
    if self._data_output_path is not None:
      data["data_output_path"] = self._data_output_path
    if self._log_path is not None:
      data["log_path"] = self._log_path

    if self._fds_endpoint is not None:
      data["fds_endpoint"] = self._fds_endpoint
    if self._fds_bucket is not None:
      data["fds_bucket"] = self._fds_bucket
    if self._hdfs_krb_account is not None and self._hdfs_endpoint is not None:
      data["hdfs_endpoint"] = self._hdfs_endpoint
      data["hdfs_krb_account"] = self._hdfs_krb_account
      if self._hdfs_krb_password is not None:
        data["hdfs_krb_password"] = self._hdfs_krb_password
      if self._hdfs_krb_keytab is not None:
        data["hdfs_krb_keytab"] = self._hdfs_krb_keytab
    if self._job_args is not None:
      data["job_args"] = self._job_args
    if (self._cpu_limit is not None):
      data["cpu_limit"] = self._cpu_limit
    if (self._memory_limit is not None):
      data["memory_limit"] = self._memory_limit
    if (self._gpu_limit is not None):
      data["gpu_limit"] = self._gpu_limit
    if self._docker_image is not None:
      data["docker_image"] = self._docker_image
    if self._docker_command is not None:
      data["docker_command"] = self._docker_command
    if self._framework is not None:
      data["framework"] = self._framework
    if self._framework_version is not None:
      data["framework_version"] = self._framework_version
    if self._volume_type is not None:
      data["volume_type"] = self._volume_type
    if self._volume_path is not None:
      data["volume_path"] = self._volume_path
    if self._mount_path is not None:
      data["mount_path"] = self._mount_path
    if self._mount_read_only is not None:
      data["mount_read_only"] = self._mount_read_only
    if self._prepare_command:
      data["prepare_command"] = self._prepare_command
    if self._finish_command:
      data["finish_command"] = self._finish_command
    if self._node_selector_key:
      data["node_selector_key"] = self._node_selector_key
    if self._node_selector_value:
      data["node_selector_value"] = self._node_selector_value
    if self._cluster_spec:
      data["cluster_spec"] = self._cluster_spec
    if self._ps_count is not None:
      data["ps_count"] = self._ps_count
    if self._worker_count is not None:
      data["worker_count"] = self._worker_count
    if self._gpu_type is not None:
      data["gpu_type"] = self._gpu_type
    if self._pipeline_id is not None:
      data["pipeline_id"] = self._pipeline_id
    if self._tensorboard_logdir is not None:
      data["tensorboard_logdir"] = self._tensorboard_logdir
    if self._model_name is not None:
      data['model_name'] = self._model_name
    if self._model_version is not None:
      data['model_version'] = self._model_version
    return json.dumps(data)
