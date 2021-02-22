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


class Schedule(object):
  """Class for schedule method.

  A schedule instance provides variables getter and setter apis. After
  specifying the necessary parameters, users can call start_run func to start
  the schedule. 
  """

  def __init__(self,
               schedule_name,
               resource_name=None,
               resource_type=None,
               cron_param=None,
               success_history_limit=None,
               failed_history_limit=None,
               suspend=None,
               concurrency_policy=None,
               image_name=None
               ):
    """Creates a new schedule with given definition.

    The `schedule_name` arguments must be provided
    when the object is creating.

    Args:
      schedule_name: The name of specific schedule.
    """
    self.schedule_name = schedule_name

    self.resource_name = resource_name
    self.resource_type = resource_type
    self.cron_param = cron_param
    self.success_history_limit = success_history_limit
    self.failed_history_limit = failed_history_limit
    self.is_suspend = suspend
    self.concurrency_policy = concurrency_policy
    self.image_name = image_name

  @property
  def schedule_name(self):
    return self._schedule_name

  @schedule_name.setter
  def schedule_name(self, value):
    """Function for setting job_name.

    Args:
      value: String type value that is going to be set to schedule_name. Which
             cannot be empty.
    Raises:
      ValueError: If value is not str instance or empty.
    """
    if not isinstance(value, str):
      raise ValueError("schedule_name must be a string!")
    if value == "":
      raise ValueError("schedule_name cannot be None!")
    if not models_util.check_kube_resource_name_regex(value):
      raise Exception("schedule_name must match {}.".format(
          models_util.kube_resource_name_regex))
    self._schedule_name = value

  @property
  def resource_name(self):
    return self._resource_name

  @resource_name.setter
  def resource_name(self, value):
    """Function for setting cloudml_endpoint.

    Args:
      value: The cloudml endpoint.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("resource name must be a string!")
    self._resource_name = value

  @property
  def resource_type(self):
    return self._resource_type

  @resource_type.setter
  def resource_type(self, value):
    if value != None:
      if not isinstance(value, str):
        raise ValueError("resource type must be a string!")
    self._resource_type=value


  @property
  def cron_param(self):
    return self._cron_param

  @cron_param.setter
  def cron_param(self, value):
    # todo validate the cronjob
    if value != None:
      if not isinstance(value, str):
        raise ValueError("cron_param must be a string!")
    self._cron_param = value

  @property
  def success_history_limit(self):
    return self._success_history_limit

  @success_history_limit.setter
  def success_history_limit(self, value):
    if value != None:
      if not isinstance(value, int):
        raise ValueError("success_history_limit must be a integer")
    self._success_history_limit = value

  @property
  def failed_history_limit(self):
    return self._failed_history_limit

  @failed_history_limit.setter
  def failed_history_limit(self, value):
    if value != None:
      if not isinstance(value, int):
        raise ValueError("Error: failed_history_limit must be a string!")
    self._failed_history_limit = value

  @property
  def is_suspend(self):
    return self._is_suspend

  @is_suspend.setter
  def is_suspend(self, value):
    self._is_suspend = value

  @property
  def concurrency_policy(self):
    return self._concurrency_policy

  @concurrency_policy.setter
  def concurrency_policy(self, value):
    if value is not None:
      if not isinstance(value, str):
        raise  ValueError("Error: concurrency_policy must be a string!")
      if value.lower() == 'forbid':
        self._concurrency_policy = 'Forbid'
      elif value.lower() == 'always':
        self._concurrency_policy = 'Always'
      elif value.lower() == 'relace':
        self._concurrency_policy = 'Replace'
      else:
        raise ValueError("Error: concurrency_policy must be the values as follows: forbid, always, replace")
    else:
      self._concurrency_policy = value

  @property
  def image_name(self):
    return self._image_name

  @image_name.setter
  def image_name(self, value):
    if value is not None:
      if not isinstance(value, str):
        raise  ValueError("Error: image_name must be a string!")
    self._image_name = value

  def get_json_data(self):
    """Get the needed schedule data after setting necessary varibles.

    Returns:
      data: The json data which is necessary for the schedule.

    """
    data = {
        "schedule_name": self._schedule_name,
    }

    if self.resource_name is not None:
      data["resource_name"] = self._resource_name

    if self.resource_type is not None:
      data["resource_type"] = self._resource_type

    if self._cron_param is not None:
      data["cron_param"] = self._cron_param
    if self._success_history_limit is not None:
      data["success_history_limit"] = self._success_history_limit
    if self._failed_history_limit is not None:
      data["failed_history_limit"] = self._failed_history_limit
    if self._is_suspend is not None:
      data["is_suspend"] = self._is_suspend
    if self._concurrency_policy is not None:
      data["concurrency_policy"] = self._concurrency_policy
    if self._image_name is not None:
      data["image_name"] = self._image_name

    return json.dumps(data)
