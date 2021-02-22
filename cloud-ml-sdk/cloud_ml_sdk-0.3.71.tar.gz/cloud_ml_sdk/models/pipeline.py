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

from cloud_ml_sdk.command.util import constant
from . import models_util
from fds import GalaxyFDSClient
from cloud_ml_sdk.client import CloudMlClient


class Pipeline(object):
  """Class for pipeline method.

  A Pipeline instance provides variables getter and setter apis. After
  specifying the necessary parameters, users can call start_run func to start
  the pipeline. 
  """

  def __init__(self,
               pipeline_name,
               fds_endpoint=None,
               fds_bucket=None,
               hdfs_krb_account=None,
               hdfs_krb_password=None,
               hdfs_endpoint=None,
               pipeline_config=None,
               org_mail=None,
               cloudml_endpoint=None,
               save_mode=False,
               create_time=None,
               update_time=None,
               hdfs_krb_keytab=None):
    """Creates a new Pipeline with given definition.

    The `pipeline_name` arguments must be provided
    when the object is creating.

    Args:
      pipeline_name: The name of specific pipeline.
    """
    self.pipeline_name = pipeline_name

    self.fds_endpoint = fds_endpoint
    self.fds_bucket = fds_bucket
    self.hdfs_krb_account = hdfs_krb_account
    self.hdfs_krb_password = hdfs_krb_password
    self.hdfs_endpoint = hdfs_endpoint
    self.pipeline_config = pipeline_config
    self.org_mail = org_mail
    self.cloudml_endpoint = cloudml_endpoint
    self.save_mode = save_mode
    self.create_time = create_time
    self.update_time = update_time
    self.hdfs_krb_keytab=hdfs_krb_keytab
  @property
  def pipeline_name(self):
    return self._pipeline_name

  @pipeline_name.setter
  def pipeline_name(self, value):
    """Function for setting job_name.

    Args:
      value: String type value that is going to be set to job_name. Which
             cannot be empty.

    Raises:
      ValueError: If value is not str instance or empty.
    """
    if not isinstance(value, str):
      raise ValueError("pipeline_name must be a string!")
    if value == "":
      raise ValueError("pipeline_name cannot be None!")
    if not models_util.check_kube_resource_name_regex(value):
      raise Exception("pipeline_name must match {}.".format(
          models_util.kube_resource_name_regex))
    self._pipeline_name = value


  @property
  def cloudml_endpoint(self):
    return self._cloudml_endpoint

  @cloudml_endpoint.setter
  def cloudml_endpoint(self, value):
    """Function for setting cloudml_endpoint.

    Args:
      value: The cloudml endpoint.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("cloudml_endpoint must be a string!")
    self._cloudml_endpoint = value

  @property
  def org_mail(self):
    return self._org_mail

  @org_mail.setter
  def org_mail(self, value):
    """Function for setting org_mail.

    Args:
      value: The org_mail.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("org_mail must be a string!")
    self._org_mail = value


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
  def hdfs_krb_keytab(self):
    return self._hdfs_krb_keytab

  @hdfs_krb_keytab.setter
  def hdfs_krb_keytab(self, value):
    if value != None:
      if not isinstance(value, str):
        raise ValueError("hdfs_krb_keytab must be a string!")
    self._hdfs_krb_keytab = value

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
  def hdfs_endpoint(self):
    return self._hdfs_endpoint

  @hdfs_endpoint.setter
  def hdfs_endpoint(self, value):
    if value != None:
      if not isinstance(value, str) or not value.startswith("hdfs://"):
        raise ValueError("hdfs_endpoint must start with hdfs://")
    self._hdfs_endpoint = value

  @property
  def save_mode(self):
    return self._save_mode

  @save_mode.setter
  def save_mode(self, value):
    self._save_mode = value

  @property
  def pipeline_config(self):
    return self._pipeline_config

  @pipeline_config.setter
  def pipeline_config(self, value):
    if value is None:
      return

    if not isinstance(value, str):
      raise ValueError("pipeline_config must be str format")
    try:
      pipeline_config_dict = json.loads(value)
    except ValueError as e:
      raise ValueError('ERROR: pipeline_config must be json format')
    if 'nodes' not in pipeline_config_dict:
      raise ValueError('ERROR: pipeline_config must contain nodes')
    #1. validate nodes format
    if not isinstance(pipeline_config_dict['nodes'], dict):
      raise ValueError('ERROR: nodes in pipeline_config must have keys')

    name_map = constant.PIPELINE_TYPE_NAME_MAP

    node_uniq_list = []
    for node_key in pipeline_config_dict['nodes']:
      if (not isinstance(pipeline_config_dict['nodes'][node_key], dict)) \
        or 'command' not in pipeline_config_dict['nodes'][node_key]:
        raise ValueError('ERROR:node in pipeline_config must be dict and  have command key')
      ''' 
      if (not isinstance(pipeline_config_dict['nodes'][node_key], dict)) \
          or 'pipeline_type' not in pipeline_config_dict['nodes'][node_key]:
        raise ValueError('ERROR:node in pipeline_config must be dict and  have pipeline_type key')
      pipeline_type = pipeline_config_dict['nodes'][node_key]['pipeline_type']

      if pipeline_type not in name_map:
        raise ValueError("ERROR:pipeline_type {} is not valid, valid type is {}".format(pipeline_type, list(name_map.keys())))

      if name_map[pipeline_type] not in pipeline_config_dict['nodes'][node_key]:
        raise ValueError('ERROR:{} node in pipeline_config must have {}'.
                         format(pipeline_type, name_map[pipeline_type]))
      pipeline_name = pipeline_config_dict['nodes'][node_key][name_map[pipeline_type]]
      if pipeline_type + pipeline_name in node_uniq_list:
        raise ValueError('ERROR: node {} in pipeline_config is duplicated'.format(node_key))
      else:
        node_uniq_list.append(pipeline_type + pipeline_name)

      if pipeline_type == constant.PIPELINE_TYPE_TRAINING:
        if 'trainer_uri' not in pipeline_config_dict['nodes'][node_key]:
          raise ValueError('ERROR: trainer_uri cant be empty when the pipeline type is {}'.format(constant.PIPELINE_TYPE_TRAINING))
        trainer_uri = str(pipeline_config_dict['nodes'][node_key]['trainer_uri'])
        # when user use the local code, auto upload
        pipeline_config_dict['nodes'][node_key]['trainer_uri'] = models_util.validate_and_get_trainer_uri(trainer_uri)
      '''
    node_keys = list(pipeline_config_dict['nodes'].keys())
    # validate edges format
    if 'edges' in pipeline_config_dict:
      for edge in pipeline_config_dict['edges']:
        if not isinstance(edge, list):
          raise ValueError('ERROR: edges in pipeline_config must be list format')
        if len(edge) < 2:
          raise ValueError('ERROR:each edge in pipeline_config must have at least 2 nodes')
        for edge_node in edge:
          if edge_node not in node_keys:
            raise ValueError('ERROR:node in edge doesn\'t exist, valid node is {}'.format("".join(node_keys)))
        # change user's input to normal format
        if len(edge) > 2:
          for i in range(len(edge)-1):
            pipeline_config_dict['edges'].append([edge[i], edge[i+1]])
          pipeline_config_dict['edges'].remove(edge)

      final_node_type = [constant.PIPELINE_TYPE_MODELSERVICE,constant.PIPELINE_TYPE_TENSORBOARD]

      for edge in pipeline_config_dict['edges']:
        first_node_key = edge[0]
        second_node_key = edge[1]
        if first_node_key == second_node_key:
          raise ValueError("Error: node in edge can't be same")

        '''
        pipeline_type = pipeline_config_dict['nodes'][first_node_key]['pipeline_type']
        if pipeline_type in final_node_type:
          raise ValueError("Error: type {} can't be the previous node of the edge.".format(pipeline_type))
        '''
    self._pipeline_config = json.dumps(pipeline_config_dict)

  @property
  def create_time(self):
    return self._create_time

  @create_time.setter
  def create_time(self, value):
    self._create_time = value

  @property
  def update_time(self):
    return self._update_time

  @update_time.setter
  def update_time(self, value):
    self._update_time = value


  def get_json_data(self):
    """Get the needed pipeline data after setting necessary varibles.

    Returns:
      data: The json data which is necessary for the pipeline.

    """
    data = {
        "pipeline_name": self._pipeline_name,
        "save_mode": self._save_mode
    }
    if self.cloudml_endpoint is not None:
      data["cloudml_endpoint"] = self._cloudml_endpoint

    if self.org_mail is not None:
      data["org_mail"] = self.org_mail
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


    if (self._pipeline_config is not None):
      data["pipeline_config"] = self._pipeline_config
    if (self._create_time is not None):
      data["create_time"] = self._create_time
    if (self._update_time is not None):
      data["update_time"] = self._update_time
    return json.dumps(data)
