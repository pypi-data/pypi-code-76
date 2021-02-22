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


class Quota(object):
  def __init__(self,
               org_id,
               org_name=None,
               org_mail = None,
               train_memory_quota=None,
               train_cpu_quota=None,
               train_gpu_quota=None,
               train_count_quota=None,
               train_priority_quota=None,
               train_priority_rank=None,
               model_memory_quota=None,
               model_cpu_quota=None,
               model_gpu_quota=None,
               model_count_quota=None,
               model_priority_quota=None,
               model_priority_rank=None,
               dev_memory_quota=None,
               dev_cpu_quota=None,
               dev_gpu_quota=None,
               dev_count_quota=None,
               dev_priority_quota=None,
               dev_priority_rank=None,
               tensorboard_quota=None,
               tensorboard_priority_quota=None,
               tensorboard_priority_rank=None,
               total_memory_quota=None,
               total_cpu_quota=None,
               total_gpu_quota=None,
               project=None):
    self.org_id = org_id
    self.org_name = org_name
    self.org_mail = org_mail
    self.train_memory_quota = train_memory_quota
    self.train_cpu_quota = train_cpu_quota
    self.train_gpu_quota = train_gpu_quota
    self.train_count_quota = train_count_quota
    self.train_priority_quota = train_priority_quota
    self.train_priority_rank = train_priority_rank
    self.model_memory_quota = model_memory_quota
    self.model_cpu_quota = model_cpu_quota
    self.model_gpu_quota = model_gpu_quota
    self.model_count_quota = model_count_quota
    self.model_priority_quota = model_priority_quota
    self.model_priority_rank = model_priority_rank
    self.dev_memory_quota = dev_memory_quota
    self.dev_cpu_quota = dev_cpu_quota
    self.dev_gpu_quota = dev_gpu_quota
    self.dev_count_quota = dev_count_quota
    self.dev_priority_quota = dev_priority_quota
    self.dev_priority_rank = dev_priority_rank
    self.tensorboard_quota = tensorboard_quota
    self.tensorboard_priority_quota = tensorboard_priority_quota
    self.tensorboard_priority_rank = tensorboard_priority_rank
    self.total_memory_quota = total_memory_quota
    self.total_cpu_quota = total_cpu_quota
    self.total_gpu_quota = total_gpu_quota
    self.project = project

  @property
  def org_id(self):
    return self._org_id

  @org_id.setter
  def org_id(self, value):
    """Function for setting org_id.

    Args:
      value: Org id.

    Raises:
      ValueError: Org_id must be a string.
    """
    if isinstance(value, str):
      self._org_id = value
    else:
      raise ValueError("org_id must be a string")

  @property
  def org_name(self):
    return self._org_name

  @org_name.setter
  def org_name(self, value):
    """Function for setting org_name.

    Args:
      value: Org name.

    Raises:
      ValueError: Org_name must be a string.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("Org_name must be a string")
    self._org_name = value

  @property
  def org_mail(self):
    return self._org_name

  @org_name.setter
  def org_mail(self, value):
    """Function for setting org_mail.

    Args:
      value: Org mail.

    Raises:
      ValueError: Org_mail must be a string.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("Org_mail must be a string")
      if not value.endswith('@xiaomi.com'):
        raise ValueError("Please enter your company mail, end with @xiaomi.com")
    self._org_mail = value

  @property
  def train_memory_quota(self):
    return self._train_memory_quota

  @train_memory_quota.setter
  def train_memory_quota(self, value):
    """Function for setting train_memory_quota.

    Args:
      value: Train memory quota.

    Raises:
      ValueError: Doesn't end with K, M or G.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("train_memory_quota must be a string")
      unit = value[-1:]
      float_value = value[:-1]
      if unit not in constant.CLOUDML_MEMORY_UNITS:
        raise ValueError("train_memory_quota unit must be one of %s!" %
                         constant.CLOUDML_MEMORY_UNITS)
      if not float_value.replace(".", "", 1).isdigit():
        raise ValueError("train_memory_quota must be a number!")
    self._train_memory_quota = value

  @property
  def train_cpu_quota(self):
    return self._train_cpu_quota

  @train_cpu_quota.setter
  def train_cpu_quota(self, value):
    """Function for setting train_cpu_quota.

    Args:
      value: Train cpu quota.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("train_cpu_quota must be a string!")
      if not value.replace(".", "", 1).isdigit():
        raise ValueError("train_cpu_quota must be a number!")
    self._train_cpu_quota = value

  @property
  def train_gpu_quota(self):
    return self._train_gpu_quota

  @train_gpu_quota.setter
  def train_gpu_quota(self, value):
    """Function for setting train_gpu_quota.

    Args:
      value: Train gpu quota.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value >= 0):
        raise ValueError("train_gpu_quota must be a nonnegative integer!")
    self._train_gpu_quota = value

  @property
  def train_count_quota(self):
    return self._train_count_quota

  @train_count_quota.setter
  def train_count_quota(self, value):
    """Function for setting train_count_quota.

    Args:
      value: Train count quota.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value > 0):
        raise ValueError("train_count_quota must be a nonnegative integer!")
    self._train_count_quota = value

  @property
  def train_priority_quota(self):
    return self._train_priority_quota

  @train_priority_quota.setter
  def train_priority_quota(self, value):
    if value != None:
      if not str(value).isdigit():
        raise ValueError("train_priority_quota must be a number!")
    self._train_priority_quota = value

  @property
  def train_priority_rank(self):
    return self._train_priority_rank

  @train_priority_rank.setter
  def train_priority_rank(self, value):
    if value != None:
      if str(value) not in constant.PRI_RANK:
        raise ValueError("Only three rank of priority (1 ,2 ,3)")
    self._train_priority_rank = value

  @property
  def model_memory_quota(self):
    return self._model_memory_quota

  @model_memory_quota.setter
  def model_memory_quota(self, value):
    """Function for setting model_memory_quota.

    Args:
      value: Model memory quota.

    Raises:
      ValueError: Doesn't end with K, M or G.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("model_memory_quota must be a string")
      unit = value[-1:]
      float_value = value[:-1]
      if unit not in constant.CLOUDML_MEMORY_UNITS:
        raise ValueError("model_memory_quota unit must be one of %s!" %
                         constant.CLOUDML_MEMORY_UNITS)
      if not float_value.replace(".", "", 1).isdigit():
        raise ValueError("model_memory_quota must be a number!")
    self._model_memory_quota = value

  @property
  def model_cpu_quota(self):
    return self._model_cpu_quota

  @model_cpu_quota.setter
  def model_cpu_quota(self, value):
    """Function for setting model_cpu_quota.

    Args:
      value: Model cpu quota.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("model_cpu_quota must be a string!")
      if not value.replace(".", "", 1).isdigit():
        raise ValueError("model_cpu_quota must be a number!")
    self._model_cpu_quota = value

  @property
  def model_gpu_quota(self):
    return self._model_gpu_quota

  @model_gpu_quota.setter
  def model_gpu_quota(self, value):
    """Function for setting model_gpu_quota.

    Args:
      value: Model gpu quota.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value >= 0):
        raise ValueError("model_gpu_quota must be a nonnegative integer!")
    self._model_gpu_quota = value

  @property
  def model_count_quota(self):
    return self._model_count_quota

  @model_count_quota.setter
  def model_count_quota(self, value):
    """Function for setting model_count_quota.

    Args:
      value: Model count quota.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value >= 0):
        raise ValueError("model_count_quota must be a nonnegative integer!")
    self._model_count_quota = value

  @property
  def model_priority_quota(self):
    return self._model_priority_quota

  @model_priority_quota.setter
  def model_priority_quota(self, value):
    if value != None:
      if not str(value).isdigit():
        raise ValueError("model_priority_quota must be a number!")
    self._model_priority_quota = value

  @property
  def model_priority_rank(self):
    return self._model_priority_rank

  @model_priority_rank.setter
  def model_priority_rank(self, value):
    if value != None:
      if str(value) not in constant.PRI_RANK:
        raise ValueError("Only three rank of priority (1 ,2 ,3)")
    self._model_priority_rank = value

  @property
  def dev_memory_quota(self):
    return self._dev_memory_quota

  @dev_memory_quota.setter
  def dev_memory_quota(self, value):
    """Function for setting dev_memory_quota.

    Args:
      value: Dev memory quota.

    Raises:
      ValueError: Doesn't end with K, M or G.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("dev_memory_quota must be a string")
      unit = value[-1:]
      float_value = value[:-1]
      if unit not in constant.CLOUDML_MEMORY_UNITS:
        raise ValueError("dev_memory_quota unit must be one of %s!" %
                         constant.CLOUDML_MEMORY_UNITS)
      if not float_value.replace(".", "", 1).isdigit():
        raise ValueError("dev_memory_quota must be a number!")
    self._dev_memory_quota = value

  @property
  def dev_cpu_quota(self):
    return self._dev_cpu_quota

  @dev_cpu_quota.setter
  def dev_cpu_quota(self, value):
    """Function for setting dev_cpu_quota.

    Args:
      value: Dev cpu quota.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("dev_cpu_quota must be a string!")
      if not value.replace(".", "", 1).isdigit():
        raise ValueError("dev_cpu_quota must be a number!")
    self._dev_cpu_quota = value

  @property
  def dev_gpu_quota(self):
    return self._dev_gpu_quota

  @dev_gpu_quota.setter
  def dev_gpu_quota(self, value):
    """Function for setting dev_gpu_quota.

    Args:
      value: Dev gpu quota.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value >= 0):
        raise ValueError("dev_gpu_quota must be a nonnegative integer!")
    self._dev_gpu_quota = value

  @property
  def dev_count_quota(self):
    return self._dev_count_quota

  @dev_count_quota.setter
  def dev_count_quota(self, value):
    """Function for setting dev_count_quota.

    Args:
      value: Dev count quota.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value >= 0):
        raise ValueError("dev_count_quota must be a nonnegative integer!")
    self._dev_count_quota = value

  @property
  def dev_priority_quota(self):
    return self._dev_priority_quota

  @dev_priority_quota.setter
  def dev_priority_quota(self, value):
    if value != None:
      if not str(value).isdigit():
        raise ValueError("dev_priority_quota must be a number!")
    self._dev_priority_quota = value

  @property
  def dev_priority_rank(self):
    return self._dev_priority_rank

  @dev_priority_rank.setter
  def dev_priority_rank(self, value):
    if value != None:
      if str(value) not in constant.PRI_RANK:
        raise ValueError("Only three rank of priority (1 ,2 ,3)")
    self._dev_priority_rank = value

  @property
  def total_memory_quota(self):
    return self._total_memory_quota

  @total_memory_quota.setter
  def total_memory_quota(self, value):
    """Function for setting total_memory_quota.

    Args:
      value: Total memory quota.

    Raises:
      ValueError: Doesn't end with K, M or G.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("total_memory_quota must be a string")
      unit = value[-1:]
      float_value = value[:-1]
      if unit not in constant.CLOUDML_MEMORY_UNITS:
        raise ValueError("total_memory_quota unit must be one of %s!" %
                         constant.CLOUDML_MEMORY_UNITS)
      if not float_value.replace(".", "", 1).isdigit():
        raise ValueError("total_memory_quota must be a number!")
    self._total_memory_quota = value

  @property
  def total_cpu_quota(self):
    return self._total_cpu_quota

  @total_cpu_quota.setter
  def total_cpu_quota(self, value):
    """Function for setting total_cpu_quota.

    Args:
      value: Total cpu quota.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("total_cpu_quota must be a string!")
      if not value.replace(".", "", 1).isdigit():
        raise ValueError("total_cpu_quota must be a number!")
    self._total_cpu_quota = value

  @property
  def total_gpu_quota(self):
    return self._total_gpu_quota

  @total_gpu_quota.setter
  def total_gpu_quota(self, value):
    """Function for setting total_gpu_quota.

    Args:
      value: Total gpu quota.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value >= 0):
        raise ValueError("total_gpu_quota must be a nonnegative integer!")
    self._total_gpu_quota = value

  @property
  def tensorboard_quota(self):
    return self._tensorboard_quota

  @tensorboard_quota.setter
  def tensorboard_quota(self, value):
    """Function for setting tensorboard_quota.

    Args:
      value: Tensorboard quota.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value >= 0):
        raise ValueError("tensorboard_quota must be a nonnegative integer!")
    self._tensorboard_quota = value

  @property
  def tensorboard_priority_quota(self):
    return self._tensorboard_priority_quota

  @tensorboard_priority_quota.setter
  def tensorboard_priority_quota(self, value):
    if value != None:
      if not str(value).isdigit():
        raise ValueError("tensorboard_priority_quota must be a number!")
    self._tensorboard_priority_quota = value

  @property
  def tensorboard_priority_rank(self):
    return self._tensorboard_priority_rank

  @tensorboard_priority_rank.setter
  def tensorboard_priority_rank(self, value):
    if value != None:
      if str(value) not in constant.PRI_RANK:
        raise ValueError("Only three rank of priority (1 ,2 ,3)")
    self._tensorboard_priority_rank = value

  def get_json_data(self):
    """Get the needed quota data after setting necessary varibles.

    Returns:
      data: The json data which is necessary for the quota.
    """
    data = {"org_id": self._org_id}
    if self._org_name is not None:
      data["org_name"] = self._org_name
    if self._org_mail is not None:
      data["org_mail"] = self._org_mail   
    if self._train_memory_quota is not None:
      data["train_memory_quota"] = self._train_memory_quota
    if self._train_cpu_quota is not None:
      data["train_cpu_quota"] = self._train_cpu_quota
    if self._train_gpu_quota is not None:
      data["train_gpu_quota"] = self._train_gpu_quota
    if self._train_count_quota is not None:
      data["train_count_quota"] = self._train_count_quota
    if self._train_priority_quota is not None:
      data["train_priority_quota"] = self._train_priority_quota
    if self._train_priority_rank is not None:
      data["train_priority_rank"] = self._train_priority_rank
    if self._model_memory_quota is not None:
      data["model_memory_quota"] = self._model_memory_quota
    if self._model_cpu_quota is not None:
      data["model_cpu_quota"] = self._model_cpu_quota
    if self._model_gpu_quota is not None:
      data["model_gpu_quota"] = self._model_gpu_quota
    if self._model_count_quota is not None:
      data["model_count_quota"] = self._model_count_quota
    if self._model_priority_quota is not None:
      data["model_priority_quota"] = self._model_priority_quota
    if self._model_priority_rank is not None:
      data["model_priority_rank"] = self._model_priority_rank
    if self._dev_memory_quota is not None:
      data["dev_memory_quota"] = self._dev_memory_quota
    if self._dev_cpu_quota is not None:
      data["dev_cpu_quota"] = self._dev_cpu_quota
    if self._dev_gpu_quota is not None:
      data["dev_gpu_quota"] = self._dev_gpu_quota
    if self._dev_count_quota is not None:
      data["dev_count_quota"] = self._dev_count_quota
    if self._dev_priority_quota is not None:
      data["dev_priority_quota"] = self._dev_priority_quota
    if self._dev_priority_rank is not None:
      data["dev_priority_rank"] = self._dev_priority_rank
    if self._tensorboard_quota is not None:
      data["tensorboard_quota"] = self.tensorboard_quota
    if self._tensorboard_priority_quota is not None:
      data["tensorboard_priority_quota"] = self._tensorboard_priority_quota
    if self._tensorboard_priority_rank is not None:
      data["tensorboard_priority_rank"] = self._tensorboard_priority_rank
    if self._total_memory_quota is not None:
      data["total_memory_quota"] = self._total_memory_quota
    if self._total_cpu_quota is not None:
      data["total_cpu_quota"] = self._total_cpu_quota
    if self._total_gpu_quota is not None:
      data["total_gpu_quota"] = self._total_gpu_quota
    if self.project is not None:
      data["project"] = self.project

    return json.dumps(data)
