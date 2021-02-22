# -*- coding: utf-8 -*-

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
import logging
import os
import requests
import sys
import yaml

import fds

from cloud_ml_common.auth.signature import Signer
from cloud_ml_sdk.command import constant

sys.path.append("../../cloud_ml_common/")
logging.basicConfig(level=logging.DEBUG)

# TODO(xychu): maybe we should consider make this a item in config file
# so if user has any complain about this dir, they could change it by their own
CLOUDML_UPLOAD_PACKAGE_DIR = "user_packages/"


class CloudMlClient(object):
  """The client to auth and operate to cloud-ml.

  A CloudMlClient instance authentic the user identity as it is created.
  And a client can handle cloud-ml job)
   methods.
  """

  def __init__(self, access_key=None, secret_key=None, endpoint=None, **kwargs):
    """Create a new CloudMlClient with given definition.

    The `access_key` and `secret_key` must be provided.

    Args:
      access_key: Access key for authentic.
      secret_key: Secret key for authentic.
    """
    config_data = self.get_config_data()

    self._secret_key = None
    self._access_key = None

    if access_key == None or secret_key == None:
      # TODO: check and catch exception
      # Get keys from environment variables
      if "XIAOMI_ACCESS_KEY_ID" in os.environ and "XIAOMI_SECRET_ACCESS_KEY" in os.environ:
        access_key = os.environ["XIAOMI_ACCESS_KEY_ID"]
        secret_key = os.environ["XIAOMI_SECRET_ACCESS_KEY"]
      else:
        if config_data:
          access_key = config_data["xiaomi_access_key_id"]
          secret_key = config_data["xiaomi_secret_access_key"]
        else:
          raise Exception(
            "Can't find access key and secret key, please run cloudml config init")

    self.access_key = access_key
    self.secret_key = secret_key

    # Declare
    self._endpoint = None
    if endpoint == None:
      if "XIAOMI_CLOUDML_ENDPOINT" in os.environ:
        self.endpoint = os.environ["XIAOMI_CLOUDML_ENDPOINT"]
      else:
        if config_data:
          self.endpoint = config_data["xiaomi_cloudml_endpoint"]
        else:
          raise Exception(
            "Can't find cloudml endpoint, please run cloudml config init")
    else:
      self.endpoint = endpoint

    if "XIAOMI_FDS_ENDPOINT" in os.environ and "CLOUDML_DEFAULT_FDS_BUCKET" in os.environ:
      self._fds_endpoint = os.environ["XIAOMI_FDS_ENDPOINT"]
      self._fds_bucket = os.environ["CLOUDML_DEFAULT_FDS_BUCKET"]
    elif config_data:
      self._fds_endpoint = config_data.get("xiaomi_fds_endpoint")
      self._fds_bucket = config_data.get("cloudml_default_fds_bucket")

    # for hdfs
    if "XIAOMI_HDFS_KRB_ACCOUNT" in os.environ and "XIAOMI_HDFS_KRB_PASSWORD" in os.environ:
      self._hdfs_krb_account = os.environ["XIAOMI_HDFS_KRB_ACCOUNT"]
      self._hdfs_krb_password = os.environ["XIAOMI_HDFS_KRB_PASSWORD"]
    elif config_data:
      self._hdfs_krb_account = config_data.get("xiaomi_hdfs_krb_account")
      self._hdfs_krb_password = config_data.get("xiaomi_hdfs_krb_password")

    if "XIAOMI_HDFS_ENDPOINT" in os.environ:
      self._hdfs_endpoint = os.environ["XIAOMI_HDFS_ENDPOINT"]
    elif config_data:
      self._hdfs_endpoint = config_data.get("xiaomi_hdfs_endpoint")

    self._auth = Signer(access_key, secret_key)

    if "xiaomi_org_mail" in kwargs and kwargs["xiaomi_org_mail"]:
      self._org_mail = kwargs["xiaomi_org_mail"]
    elif "XIAOMI_ORG_MAIL" in os.environ:
      self._org_mail = os.environ["XIAOMI_ORG_MAIL"]
    elif config_data and "xiaomi_org_mail" in config_data:
      self._org_mail = config_data.get("xiaomi_org_mail")
    else:
      raise Exception(
        "Can't find org mail, please set one by re-run 'cloudml config init'")

  def get_config_data(self):
    # Read keys from configuration file
    data = {}
    try:
      config_filename = os.path.join(
        os.path.expanduser("~"), constant.CONFIG_PATH, constant.CONFIG_FILENAME)
      if os.path.exists(config_filename):
        with open(config_filename) as f:
          data = yaml.safe_load(f)
    except Exception as e:
      raise ValueError(
        "Failed to load config data, is the json data in right format? Exception content: {}".format(
          e))
    try:
      if constant.CLOUDML_CONFIG_KEY in data:
        # NOTE(xychu): XIAOMI_CLOUDML_CONFIG_CONTEXT Env will be set by cloudml -k/--context arg
        if "XIAOMI_CLOUDML_CONFIG_CONTEXT" in os.environ:
          config_context_name = os.environ["XIAOMI_CLOUDML_CONFIG_CONTEXT"]
          if config_context_name in data[constant.CLOUDML_CONFIG_KEY]:
            # load user demand context config
            context_config = data[constant.CLOUDML_CONFIG_KEY][config_context_name]
            data.update(context_config)
          else:
            # user demand config context not found
            raise ValueError(
              "Config context with name {} not found.\n".format(config_context_name) +
              "Please set a valid one or init it first.")
        else:
          # load default context specific config
          if constant.DEFAULT_CONFIG_CONTEXT in data[constant.CLOUDML_CONFIG_KEY]:
            default_cluster = data[constant.CLOUDML_CONFIG_KEY][constant.DEFAULT_CONFIG_CONTEXT]
            context_config = data[constant.CLOUDML_CONFIG_KEY][default_cluster]
            data.update(context_config)
          elif len(data[constant.CLOUDML_CONFIG_KEY]) == 1:
            # if there's only one config context, use it as default
            for default_cluster in data[constant.CLOUDML_CONFIG_KEY]:
              context_config = data[constant.CLOUDML_CONFIG_KEY][default_cluster]
              data.update(context_config)
          else:
            raise ValueError(
              "No default config context found. \n" +
              "Please set your default context by: cloudml config set_default <name_of_your_config_context>")
    except Exception as e:
      raise ValueError(
        "Failed to load context config. Exception content: {}".format(
          e))
    return data

  @property
  def access_key(self):
    return self._access_key

  @access_key.setter
  def access_key(self, value):
    """Function for setting access_key.
    """
    if not isinstance(value, str):
      raise ValueError("access_key must be a string!")
    self._access_key = value

  @property
  def secret_key(self):
    return self._secret_key

  @secret_key.setter
  def secret_key(self, value):
    """Function for setting secret_key.
    """
    if not isinstance(value, str):
      raise ValueError("secret_key must be a string!")
    self._secret_key = value

  @property
  def endpoint(self):
    return self._endpoint

  @endpoint.setter
  def endpoint(self, value):
    """Function for setting endpoint.

    Args:
      value: String value that is going to be set to endpoint.
    """
    if not isinstance(value, str):
      raise ValueError("endpoint must be a string!")
    if not (value.startswith("http://") or value.startswith("https://")):
      value = "https://" + value
    self._endpoint = value
    self._hp_url = self._endpoint + "/cloud_ml/v1/hp"
    self._train_url = self._endpoint + "/cloud_ml/v1/train"
    self._model_url = self._endpoint + "/cloud_ml/v1/model"
    self._dev_url = self._endpoint + "/cloud_ml/v1/dev"
    self._tensorboard_url = self._endpoint + "/cloud_ml/v1/tensorboard"
    self._quota_url = self._endpoint + "/cloud_ml/v1/quota"
    self._quota_application_url = self._endpoint + "/cloud_ml/v1/application"
    self._framework_url = self._endpoint + "/cloud_ml/v1/framework"
    self._authentication_url = self._endpoint + "/cloud_ml/v1/authentication"
    self._org_id_url = self._endpoint + "/cloud_ml/v1/org_ids"
    self._dev_server_url = self._endpoint + "/dev_server/v1/dev_servers"
    self._pipeline_url = self._endpoint + "/cloud_ml/v1/pipeline"
    self._schedule_url = self._endpoint + "/cloud_ml/v1/schedule"
    self._resources_url = self._endpoint + "/cloud_ml/v1/resources"
    self._ceph_url = self._endpoint + "/cloud_ml/v1/ceph"
    self._secret_url = self._endpoint + "/cloud_ml/v1/secret"
    self._namespace_url = self._endpoint + "/cloud_ml/v1/namespace"
    self._namespace_quota_url = self._endpoint + "/cloud_ml/v1/namespace_quota"
    self._namespace_user_url = self._endpoint + "/cloud_ml/v1/namespace_user"

  @property
  def fds_endpoint(self):
    return self._fds_endpoint

  @fds_endpoint.setter
  def fds_endpoint(self, value):
    """Function for setting xiaomi_fds_endpoint.
    """
    if not isinstance(value, str):
      raise ValueError("fds_endpoint must be a string!")
    self._fds_endpoint = value

  @property
  def org_mail(self):
    return self._org_mail

  @org_mail.setter
  def org_mail(self, value):
    """Function for setting xiaomi_org_mail.
    """
    if not isinstance(value, str):
      raise ValueError("org_mail must be a string!")
    self._org_mail = value

  @property
  def fds_bucket(self):
    return self._fds_bucket

  @fds_bucket.setter
  def fds_bucket(self, value):
    """Function for setting cloudml_default_fds_bucket.
    """
    if not isinstance(value, str):
      raise ValueError("fds_bucket must be a string!")
    self._fds_bucket = value

  # for hdfs
  @property
  def hdfs_krb_account(self):
    return self._hdfs_krb_account

  @hdfs_krb_account.setter
  def hdfs_krb_account(self, value):
    if not isinstance(value, str):
      raise ValueError("hdfs_krb_account must be a string!")
    self._hdfs_krb_account = value

  @property
  def hdfs_krb_password(self):
    return self._hdfs_krb_password

  @hdfs_krb_password.setter
  def hdfs_krb_password(self, value):
    if not isinstance(value, str):
      raise ValueError("hdfs_krb_password must be a string!")
    self._hdfs_krb_password = value

  @property
  def hdfs_endpoint(self):
    return self._hdfs_endpoint

  @hdfs_endpoint.setter
  def hdfs_endpoint(self, value):
    if not isinstance(value, str) or value.startswith("hdfs://"):
      raise ValueError("hdfs_endpoint must start with hdfs://")
    self._hdfs_endpoint = value

  def get_fds_client(self):
    """Init FDS client with correct configuration including: ak, sk, fds_endpoint.

    :return: GalaxyFDSClient or ValueError
    """
    fds_client = None
    try:
      fds_config = fds.FDSClientConfiguration()
      fds_config.set_endpoint(self.fds_endpoint)
      fds_client = fds.GalaxyFDSClient(self.access_key, self.secret_key, fds_config)
    except Exception as e:
      raise ValueError("Init FDS client got error: {}".format(e))
    else:
      return fds_client

  # For hptuning
  def submit_hptuning(self, json_data):
    response = requests.post(self._hp_url, auth=self._auth, data=json_data)
    return self.process_response(response)

  def delete_hp_job(self, hp_name, org_id=None):
    """Delete the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The response.
    """
    if org_id:
      url = self._hp_url + "/" + hp_name + "?org_id=" + org_id
    else:
      url = self._hp_url + "/" + hp_name
    response = requests.delete(url, auth=self._auth)
    return self.process_response(response)

  def list_hp_jobs(self, org_id=None):
    """List hp jobs.

    Args:
      The org_id whose hp_jobs to list.

    Returns:
      The list of dictionary of hp jobs.
    """
    if org_id:
      url = self._hp_url + "?org_id=" + org_id
    else:
      url = self._hp_url
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def list_hp_trials(self, hp_name, org_id=None):
    """List hp jobs'trials.

    Args:
      The org_id whose hp jobs' trials to list.

    Returns:
      The list of dictionary of trials.
    """
    if org_id:
      url = self._hp_url + "/" + hp_name + "/trials" + "?org_id=" + org_id
    else:
      url = self._hp_url + "/" + hp_name + "/trials"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def get_hp_trial_logs(self, hp_name, trial_id, org_id=None, follow=False, lines=None):
    """Get logs of the hp trial.

        Args:
          hp_name: The name of the hp job.
          trial_id: The id of the trial(pod)

        Returns:
          The logs of trial.
        """
    params = {}
    if org_id:
      params['org_id'] = org_id
    if follow:
      params['follow'] = follow
    if lines:
      params['lines'] = lines

    url = self._hp_url + "/" + hp_name + "/" + trial_id + "/logs"
    return requests.get(url, params=params, auth=self._auth, stream=follow)

  def describe_hp_job(self, hp_name, org_id=None):
    """Describe and get information of the hp job.

    Args:
      Hp_name: The name of the hpjob.

    Returns:
      The dictionary of hp job.
    """
    if org_id:
      url = self._hp_url + "/" + hp_name + "?org_id=" + org_id
    else:
      url = self._hp_url + "/" + hp_name
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def get_hp_job_events(self, hp_name, org_id=None):
    """Get events of the hp job.

    Args:
      hp_name: The name of the hp job.

    Returns:
      The events of the hp job.
    """
    if org_id:
      url = self._hp_url + "/" + hp_name + "/events" + "?org_id=" + org_id
    else:
      url = self._hp_url + "/" + hp_name + "/events"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def get_hp_job_metrics(self, hp_name, org_id=None):
    """Get the metrics of the hp job.

    Args:
      hp_name: The name of the hp job.

    Returns:
      The logs of hp job.
    """
    if org_id:
      url = self._hp_url + "/" + hp_name + "/metrics" + "?org_id=" + org_id
    else:
      url = self._hp_url + "/" + hp_name + "/metrics"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def submit_train_job(self, json_data):
    """Submit a train_job to run.

    Args:
      json_data: The json data of train job to submit.

    Returns:
      The dictionary of train job.
    """
    response = requests.post(self._train_url, auth=self._auth, data=json_data)
    return self.process_response(response)

  def list_train_jobs(self, org_id=None):
    """List train jobs.

    Args:
      The org_id whose train_jobs to list.

    Returns:
      The list of dictionary of train jobs.
    """
    if org_id:
      url = self._train_url + "?org_id=" + org_id
    else:
      url = self._train_url
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def describe_train_job(self, job_name, org_id=None):
    """Describe and get information of the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The dictionary of train job.
    """
    if org_id:
      url = self._train_url + "/" + job_name + "?org_id=" + org_id
    else:
      url = self._train_url + "/" + job_name
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def get_train_job_logs(self, job_name, org_id=None, follow=False, lines=None):
    """Get logs of the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The logs of train job.
    """
    params = {}
    if org_id:
      params['org_id'] = org_id
    if follow:
      params['follow'] = follow
    if lines:
      params['lines'] = lines

    url = self._train_url + "/" + job_name + "/logs"
    return requests.get(url, params=params, auth=self._auth, stream=follow)

  def get_train_job_metrics(self, job_name, org_id=None):
    """Get the metrics of the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The logs of train job.
    """
    if org_id:
      url = self._train_url + "/" + job_name + "/metrics" + "?org_id=" + org_id
    else:
      url = self._train_url + "/" + job_name + "/metrics"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def get_train_job_hyperparameters_data(self, job_name):
    """Get hyperparameters data of the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The hyperparameter data of train job.
    """
    url = self._train_url + "/" + job_name + "/hyperparameters"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def delete_train_job(self, job_name, org_id=None, is_cluster_name=False):
    """Delete the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The response.
    """
    params = {}
    if is_cluster_name:
      params["is_cluster_name"] = is_cluster_name
    if org_id:
      url = self._train_url + "/" + job_name + "?org_id=" + org_id
    else:
      url = self._train_url + "/" + job_name
    response = requests.delete(url, auth=self._auth, params=params)
    return self.process_response(response)

  def get_train_job_events(self, job_name, org_id=None):
    """Get events of the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The events of the train job.
    """
    if org_id:
      url = self._train_url + "/" + job_name + "/events" + "?org_id=" + org_id
    else:
      url = self._train_url + "/" + job_name + "/events"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def start_train_job(self, job_name):
    """Start the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The dictionary of train job.
    """
    url = self._train_url + "/" + job_name + "/start"
    response = requests.get(url, auth=self._auth)

    return self.process_response(response)

  def create_model_service(self, model_service):
    """Create the model service.

    Args:
      model_service: The model service object to create.

    Returns:
      The dictionary of model service.
    """
    model_service_data = model_service.get_json_data()
    response = requests.post(self._model_url,
                             auth=self._auth,
                             data=model_service_data)
    return self.process_response(response)

  def list_model_services(self, org_id=None):
    """List model services.

    Returns:
      The list of dictionary of model services.
    """
    if org_id:
      url = self._model_url + "?org_id=" + org_id
    else:
      url = self._model_url
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def start_model_service(self, model_name, model_version):
    """Start the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.

    Returns:
      The dictionary of model service.
    """
    url = self._model_url + "/" + model_name + "/" + model_version + "/start"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def describe_model_service(self, model_name, model_version, org_id=None):
    """Describe and get information of the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.

    Returns:
      The dictionary of model service.
    """
    if org_id:
      url = self._model_url + "/" + model_name + "/" + model_version + "?org_id=" + org_id
    else:
      url = self._model_url + "/" + model_name + "/" + model_version
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def update_model_service(self, model_name, model_version, update_json, org_id=None):
    """Describe and get information of the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.
      update_json: The json data to update the model service.

    Returns:
      The dictionary of model service.
    """
    if org_id:
      url = self._model_url + "/" + model_name + "/" + model_version + "?org_id=" + org_id
    else:
      url = self._model_url + "/" + model_name + "/" + model_version
    response = requests.put(url, auth=self._auth, data=update_json)
    return self.process_response(response)

  def get_model_service_logs(self, model_name, model_version, org_id=None, replica_index=None, proxy_logs=None):
    """Get logs of the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.
      org_id: the client's orgid
      replica_index: the replica's index,

    Returns:
      The logs of the model service.
    """
    if org_id:
      if replica_index:
        url = self._model_url + "/" + model_name + "/" + model_version + "/logs" + "?org_id=" + org_id + \
              "&replica=" + replica_index
      elif proxy_logs:
        url = self._model_url + "/" + model_name + "/" + model_version + "/logs" + "?org_id=" + org_id + \
              "&proxy=" + "1"
      else:
        url = self._model_url + "/" + model_name + "/" + model_version + "/logs" + "?org_id=" + org_id
    else:
      if replica_index:
        url = self._model_url + "/" + model_name + "/" + model_version + "/logs" + "?replica=" + replica_index
      elif proxy_logs:
        url = self._model_url + "/" + model_name + "/" + model_version + "/logs" + "?proxy=" + "1"
      else:
        url = self._model_url + "/" + model_name + "/" + model_version + "/logs"

    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def get_model_service_metrics(self, model_name, model_version, org_id=None):
    """Get the metrics of the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.

    Returns:
      The logs of the model service.
    """
    if org_id:
      url = self._model_url + "/" + model_name + "/" + model_version + "/metrics" + "?org_id=" + org_id
    else:
      url = self._model_url + "/" + model_name + "/" + model_version + "/metrics"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def delete_model_service(self, model_name, model_version, org_id=None):
    """Delete the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.

    Returns:
      The response.
    """
    url = self._model_url + "/" + model_name + "/" + model_version
    if org_id:
      url = url + "?org_id=" + org_id
    response = requests.delete(url, auth=self._auth)
    return self.process_response(response)

  def get_model_service_events(self, model_name, model_version, org_id=None):
    """Get events of the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.

    Returns:
      The events of the model service.
    """
    if org_id:
      url = self._model_url + "/" + model_name + "/" + model_version + "/events" + "?org_id=" + org_id
    else:
      url = self._model_url + "/" + model_name + "/" + model_version + "/events"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def create_dev_env(self, dev_env_data):
    """Create the dev env.

    Args:
      dev_env: The dev env object to submit.

    Returns:
      The dictionary of dev env.
    """
    response = requests.post(self._dev_url, auth=self._auth, data=dev_env_data)
    return self.process_response(response)

  def list_dev_envs(self, org_id=None):
    """List the dev environments.

    Returns:
      The list of dictionary of dev env.
    """
    if org_id:
      url = self._dev_url + "?org_id=" + org_id
    else:
      url = self._dev_url
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def describe_dev_env(self, dev_name, org_id=None):
    """Describe and get information of the dev environment.

    Args:
      dev_name: The name of the dev environment.

    Returns:
      The dictionary of dev environment.
    """
    url = self._dev_url + "/" + dev_name
    if org_id:
      url = url + "?org_id=" + org_id
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def delete_dev_env(self, dev_name, org_id=None):
    """Delete the dev environment.

    Args:
      dev_name: The name of the dev environment.

    Returns:
      The response.
    """
    url = self._dev_url + "/" + dev_name
    if org_id:
      url = url + "?org_id=" + org_id
    response = requests.delete(url, auth=self._auth)
    return self.process_response(response)

  def stop_dev_env(self, dev_name, org_id=None):
    """Stop the dev env.

    Args:
      dev_name: The name of the dev environment.

    Returns:
      The events of the dev env.
    """
    url = self._dev_url + "/" + dev_name + "/stop"
    if org_id:
      url = url + "?org_id=" + org_id
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def save_dev_env(self, dev_name, org_id=None):
    """Save the dev env.

    Args:
      dev_name: The name of the dev environment.

    Returns:
      The events of the dev env.
    """
    url = self._dev_url + "/" + dev_name + "/save"
    if org_id:
      url = url + "?org_id=" + org_id
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def restart_dev_env(self, dev_name, org_id=None):
    """Restart the dev env.

    Args:
      dev_name: The name of the dev environment.

    Returns:
      The events of the dev env.
    """
    url = self._dev_url + "/" + dev_name + "/restart"
    if org_id:
      url = url + "?org_id=" + org_id
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def get_dev_env_events(self, dev_name):
    """Get events of the dev env.

    Args:
      dev_name: The name of the dev environment.

    Returns:
      The events of the dev env.
    """
    url = self._dev_url + "/" + dev_name + "/events"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def get_dev_env_metrics(self, dev_name):
    """Get the metrics of the dev env.

    Args:
      dev_name: The name of the dev environment.

    Returns:
      The events of the dev env.
    """
    url = self._dev_url + "/" + dev_name + "/metrics"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def create_dev_server(self, dev_server):
    """Create the dev server.

    Args:
      dev_server: The dev server object to submit.

    Returns:
      The dictionary of dev server.
    """
    dev_server_data = dev_server.get_json_data()
    response = requests.post(self._dev_server_url,
                             auth=self._auth,
                             data=dev_server_data)
    return self.process_response(response)

  def list_dev_servers(self, org_id=None):
    """List the dev servers.

    Returns:
      The list of dictionary of dev server.
    """
    if org_id:
      url = self._dev_server_url + "?org_id=" + org_id
    else:
      url = self._dev_server_url
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def describe_dev_server(self, dev_name, org_id=None):
    """Describe and get information of the dev server.

    Args:
      dev_name: The name of the dev server.

    Returns:
      The dictionary of dev server.
    """
    if org_id:
      url = self._dev_server_url + "/" + dev_name + "?org_id=" + org_id
    else:
      url = self._dev_server_url + "/" + dev_name
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def delete_dev_server(self, dev_name):
    """Delete the dev server.

    Args:
      dev_name: The name of the dev server.

    Returns:
      The response.
    """
    url = self._dev_server_url + "/" + dev_name
    response = requests.delete(url, auth=self._auth)
    return self.process_response(response)

  def get_dev_server_events(self, dev_name):
    """Get events of the dev server.

    Args:
      dev_name: The name of the dev server.

    Returns:
      The events of the dev server.
    """
    url = self._dev_server_url + "/" + dev_name + "/events"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def create_tensorboard_service(self, tensorboard_service):
    """Create the tensorboard_service.

    Args:
      tensorboard_service: The tensorboard_service object to create.

    Returns:
      The dictionary of tensorboard_service.
    """
    tensorboard_service_data = tensorboard_service.get_json_data()
    response = requests.post(self._tensorboard_url,
                             auth=self._auth,
                             data=tensorboard_service_data)
    return self.process_response(response)

  def list_tensorboard_services(self, org_id=None):
    """List tensorboard_services.

    Returns:
      The list of dictionary of tensorboard_services.
    """
    if org_id:
      url = self._tensorboard_url + "?org_id=" + org_id
    else:
      url = self._tensorboard_url
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def describe_tensorboard_service(self, tensorboard_name, org_id=None):
    """Describe and get information of the tensorboard_service.

    Args:
      tensorboard_name: The name of the tensorboard_service.

    Returns:
      The dictionary of tensorboard_service.
    """
    if org_id:
      url = self._tensorboard_url + "/" + tensorboard_name + "?org_id=" + org_id
    else:
      url = self._tensorboard_url + "/" + tensorboard_name
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def delete_tensorboard_service(self, tensorboard_name, org_id=None):
    """Delete the tensorboard_service.

    Args:
      tensorboard_name: The name of the tensorboard_service.

    Returns:
      The response.
    """
    url = self._tensorboard_url + "/" + tensorboard_name
    if org_id:
      url = url + "?org_id=" + org_id
    response = requests.delete(url, auth=self._auth)
    return self.process_response(response)

  def get_tensorboard_service_events(self, tensorboard_name):
    """Get events of the tensorboard service.

    Args:
      tensorboard_name: The name of the tensorboard service.

    Returns:
      The events of the tensorboard service.
    """
    url = self._tensorboard_url + "/" + tensorboard_name + "/events"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def create_pipeline_schedule(self, json_data, pipeline_name):
    url = self._pipeline_url + '/' + pipeline_name + "/schedule"
    response = requests.post(url, auth=self._auth, data=json_data)
    return self.process_response(response)

  def list_pipeline_schedules(self, pipeline_name, org_id=None):
    if org_id:
      url = self._pipeline_url + '/' + pipeline_name + "/schedule?org_id=" + org_id
    else:
      url = self._pipeline_url + '/' + pipeline_name + "/schedule"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def describe_pipeline_schedule(self, pipeline_schedule_id, org_id=None):
    if org_id:
      url = self._pipeline_url + '/schedule/' + pipeline_schedule_id +"?org_id=" + org_id
    else:
      url = self._pipeline_url + '/schedule/' + pipeline_schedule_id
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)


  def delete_pipeline(self, pipeline_name):
    """Delete the pipeline.

    Args:
      pipeline_name: The name of the pipeline.
    Returns:
      The response.
    """
    url = self._pipeline_url + "/" + pipeline_name

    response = requests.delete(url, auth=self._auth)
    return self.process_response(response)


  def list_pipelines(self, org_id=None):
    if org_id:
      url = self._pipeline_url + "?org_id=" + org_id
    else:
      url = self._pipeline_url
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def delete_pipeline(self, pipeline_name):
    """Delete the pipeline.

    Args:
      pipeline_name: The name of the pipeline.
    Returns:
      The response.
    """
    url = self._pipeline_url + "/" + pipeline_name

    response = requests.delete(url, auth=self._auth)
    return self.process_response(response)

  def describe_pipeline(self, pipeline_name, org_id=None):
    """Describe and get information of the pipeline.

    Args:
      pipeline_name: The name of the pipeline.

    Returns:
      The dictionary of pipeline.
    """
    if org_id:
      url = self._pipeline_url + "/" + pipeline_name + "?org_id=" + org_id
    else:
      url = self._pipeline_url + "/" + pipeline_name
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def get_pipeline_logs(self, pod_name, org_id=None):
    """Get logs of the pipeline.

    Args:
      pipeline_name: The pod name of the pipeline.

    Returns:
      The logs of pipeline pod.
    """
    if org_id:
      url = self._pipeline_url + "/" + pod_name + "/logs" + "?org_id=" + org_id
    else:
      url = self._pipeline_url + "/" + pod_name + "/logs"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def start_pipeline(self, pipeline_name, org_id=None):
    if org_id:
      url = self._pipeline_url + "/" + pipeline_name + "/start" + "?org_id=" + org_id
    else:
      url = self._pipeline_url + "/" + pipeline_name + "/start"
    response = requests.put(url, auth=self._auth)
    return self.process_response(response)

  def stop_pipeline(self, pipeline_name, org_id=None):
    if org_id:
      url = self._pipeline_url + "/" + pipeline_name + "/stop" + "?org_id=" + org_id
    else:
      url = self._pipeline_url + "/" + pipeline_name + "/stop"
    response = requests.put(url, auth=self._auth)
    return self.process_response(response)

  def rerun_pipeline(self, pipeline_name, json_data):
    url = self._pipeline_url + "/" + pipeline_name + "/rerun"
    response = requests.post(url, auth=self._auth, data=json_data)
    return self.process_response(response)

  def create_pipeline(self, json_data):
    """Submit a pipeline to run.

    Args:
      json_data: The json data of pipeline to submit.

    Returns:
      The dictionary of pipeline.
    """
    response = requests.post(self._pipeline_url, auth=self._auth, data=json_data)
    return self.process_response(response)

  def update_pipeline(self, json_data, pipeline_name):
    """Submit a pipeline to run.

    Args:
      json_data: The json data of pipeline to submit.

    Returns:
      The dictionary of pipeline.
    """
    url = self._pipeline_url + "/" + pipeline_name
    response = requests.put(url, auth=self._auth, data=json_data)
    return self.process_response(response)

  def list_schedules(self, org_id=None):
    if org_id:
      url = self._schedule_url + "?org_id=" + org_id
    else:
      url = self._schedule_url
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def delete_schedule(self, schedule_name):
    """Delete the schedule.

    Args:
      schedule_name: The name of the schedule.
    Returns:
      The response.
    """
    url = self._schedule_url + "/" + schedule_name

    response = requests.delete(url, auth=self._auth)
    return self.process_response(response)

  def describe_schedule(self, schedule_name, org_id=None):
    """Describe and get information of the schedule.

    Args:
      schedule_name: The name of the schedule.

    Returns:
      The dictionary of schedule.
    """
    if org_id:
      url = self._schedule_url + "/" + schedule_name + "?org_id=" + org_id
    else:
      url = self._schedule_url + "/" + schedule_name
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)


  def start_schedule(self, schedule_name, org_id=None):
    if org_id:
      url = self._schedule_url + "/" + schedule_name + "/start" + "?org_id=" + org_id
    else:
      url = self._schedule_url + "/" + schedule_name + "/start"
    response = requests.put(url, auth=self._auth)
    return self.process_response(response)

  def stop_schedule(self, schedule_name, org_id=None):
    if org_id:
      url = self._schedule_url + "/" + schedule_name + "/stop" + "?org_id=" + org_id
    else:
      url = self._schedule_url + "/" + schedule_name + "/stop"
    response = requests.put(url, auth=self._auth)
    return self.process_response(response)

  def create_schedule(self, json_data):
    """Submit a schedule to run.

    Args:
      json_data: The json data of schedule to submit.

    Returns:
      The dictionary of schedule.
    """
    response = requests.post(self._schedule_url, auth=self._auth, data=json_data)
    return self.process_response(response)

  def update_schedule(self, json_data, schedule_name):
    """Update a schedule to run.

    Args:
      json_data: The json data of schedule to submit.

    Returns:
      The dictionary of schedule.
    """
    url = self._schedule_url + "/" + schedule_name
    response = requests.put(url, auth=self._auth, data=json_data)
    return self.process_response(response)


  def create_ceph_service(self, ceph_service):
    """Create the ceph_service.

    Args:
      ceph_service: The ceph_service object to create.

    Returns:
      The dictionary of ceph_service.
    """
    ceph_service_data = ceph_service.get_json_data()
    response = requests.post(self._ceph_url,
                             auth=self._auth,
                             data=ceph_service_data)
    return self.process_response(response)

  def list_ceph_services(self, org_id=None):
    """List ceph_services.

    Returns:
      The list of dictionary of ceph_services.
    """
    if org_id:
      url = self._ceph_url + "?org_id=" + org_id
    else:
      url = self._ceph_url
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def describe_ceph_service(self, ceph_name, org_id=None):
    """Describe and get information of the ceph_service.

    Args:
      ceph_name: The name of the ceph_service.

    Returns:
      The dictionary of ceph_service.
    """
    if org_id:
      url = self._ceph_url + "/" + ceph_name + "?org_id=" + org_id
    else:
      url = self._ceph_url + "/" + ceph_name
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def delete_ceph_service(self, ceph_name, org_id=None, force=False):
    """Delete the ceph_service.

    Args:
      ceph_name: The name of the ceph_service.

    Returns:
      The response.
    """
    url = self._ceph_url + "/" + ceph_name
    if org_id != None:
      url = url + "?org_id=" + org_id
    if force != None:
      url = url + "?force=" + str(force)
    response = requests.delete(url, auth=self._auth)
    return self.process_response(response)

  def get_ceph_service_events(self, ceph_name):
    """Get events of the ceph service.

    Args:
      ceph_name: The name of the ceph service.

    Returns:
      The events of the ceph service.
    """
    url = self._ceph_url + "/" + ceph_name + "/events"
    response = requests.get(url, auth=self._auth)
    return self.process_response(response)

  def get_quota(self, org_id=None):
    """Get quota.
    """
    # NOTE(jishaomin): cloudml_admin command corresponds to org_id, cloudml command corresponds to no org_id
    if org_id:
      url = self._quota_url + "?org_id=" + org_id
      response = requests.get(url, auth=self._auth)
    else:
      url = self._quota_url
      body = {}
      body['org_mail'] = self._org_mail
      body = json.dumps(body)
      response = requests.post(url, auth=self._auth, data=body)

    return self.process_response(response, 'data')

  def do_predict(self, model_name, model_version, data_file, timeout=10.0):
    """Request generic gRPC server to predict

    Args:
      model_name: The name of the model.
      model_version: The version of the model.
      data_file: The json data file.
      timeout: The timeout of the gRPC request.
    """
    model_service = self.describe_model_service(model_name, model_version)
    if type(model_service) is dict:
      server = model_service["address"]
      return self.do_predict_server(server, model_name, data_file, timeout)
    else:
      return json.dumps({
        "error": True,
        "message": "Fail to get information of model service"
      })

  def do_predict_server(self, server, model_name, data_file, timeout=10.0):

    from .predict_client import generic_predict_client

    if os.path.isfile(data_file):
      with open(data_file) as f:
        data = json.load(f)
    else:
      return {
        "error": True,
        "message": "The data file: {} doesn't exist".format(data_file)
      }

    return generic_predict_client.predict(server, model_name, data, timeout)

  def update_quota(self, quota):
    """Update quota by admin.

    Args:
      quota: The quota object with new value.
    """
    quota_data = quota.get_json_data()
    url = self._quota_url + "/" + quota.org_id
    response = requests.put(url, auth=self._auth, data=quota_data)
    return self.process_response(response)

  def apply_quota(self, quota_data):
    """Update quota by admin.

    Args:
      quota: The quota object with new value.
    """
    url = self._quota_application_url + "?org_id=" + quota_data["org_id"]
    body = json.dumps(quota_data)
    response = requests.post(url,
                             auth=self._auth,
                             data=body)
    return self.process_response(response)

  def create_secret_service(self, secret_service):
    """Create the secret_service.

    Args:
      secret_service: The secret_service object to create.

    Returns:
      The dictionary of secret_service.
    """
    secret_service_data = secret_service.get_json_data()
    response = requests.post(self._secret_url,
                             auth=self._auth,
                             data=secret_service_data)
    return self.process_response(response, 'data')

  def list_secret_services(self, org_id=None):
    """List secret_services.

    Returns:
      The list of dictionary of secret_services.
    """
    if org_id:
      url = self._secret_url + "?org_id=" + org_id
    else:
      url = self._secret_url
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def describe_secret_service(self, secret_name, org_id=None):
    """Describe and get information of the secret_service.

    Args:
      secret_name: The name of the secret_service.
      org_id: The org_id of the secret_service

    Returns:
      The dictionary of secret_service.
    """
    if org_id:
      url = self._secret_url + "/" + secret_name + "?org_id=" + org_id
    else:
      url = self._secret_url + "/" + secret_name
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def delete_secret_service(self, secret_name, org_id=None):
    """Delete the secret_service.

    Args:
      secret_name: The name of the secret_service.
      org_id: The org_id of the secret_service

    Returns:
      The response.
    """
    url = self._secret_url + "/" + secret_name
    if org_id:
      url = url + "?org_id=" + org_id
    response = requests.delete(url, auth=self._auth)
    return self.process_response(response)

  def create_namespace(self, namespace):
    """Create the namespace.

    Args:
      namespace: The namespace object to create.

    Returns:
      The dictionary of namespace.
    """
    namespace_json = namespace.get_json_data()
    response = requests.post(self._namespace_url,
                             auth=self._auth,
                             data=namespace_json)
    return self.process_response(response, 'data')

  def update_namespace(self, namespace):
    """Update the namespace.

    Args:
      namespace: The namespace object to create.

    Returns:
      The dictionary of namespace.
    """
    namespace_json = namespace.get_json_data()
    response = requests.patch(self._namespace_url,
                              auth=self._auth,
                              data=namespace_json)
    return self.process_response(response, 'data')

  def list_namespaces(self):
    """List namespaces.

    Returns:
      The list of dictionary of namespace.
    """
    response = requests.get(self._namespace_url, auth=self._auth)
    return self.process_response(response, 'data')

  def describe_namespace(self, name):
    """Describe and get information of the namespace.

    Args:
      name: The name of the namespace.

    Returns:
      The dictionary of namespace.
    """
    url = self._namespace_url + "/" + name
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def delete_namespace(self, name):
    """Delete the namespace.

    Args:
      name: The name of the namespace.

    Returns:
      The response.
    """
    url = self._namespace_url + "/" + name
    response = requests.delete(url, auth=self._auth)
    return self.process_response(response)

  def create_namespace_quota(self, namespace_quota):
    """Create the namespace quota.

    Args:
      namespace_quota: The namespace quota object to create/update.

    Returns:
      The dictionary of namespace quota.
    """
    namespace_quota_json = namespace_quota.get_json_data()
    response = requests.post(self._namespace_quota_url,
                             auth=self._auth,
                             data=namespace_quota_json)
    return self.process_response(response, 'data')

  def update_namespace_quota(self, namespace_quota):
    """Update the namespace quota.

    Args:
      namespace_quota: The namespace quota object to create/update.

    Returns:
      The dictionary of namespace quota.
    """
    namespace_quota_json = namespace_quota.get_json_data()
    response = requests.patch(self._namespace_quota_url,
                             auth=self._auth,
                             data=namespace_quota_json)
    return self.process_response(response, 'data')

  def list_namespace_quotas(self):
    """List namespace quotas.

    Returns:
      The list of dictionary of namespace quota.
    """
    response = requests.get(self._namespace_quota_url, auth=self._auth)
    return self.process_response(response, 'data')

  def describe_namespace_quota(self, name):
    """Describe and get information of the namespace quota.

    Args:
      name: The name of the namespace.

    Returns:
      The dictionary of namespace quota.
    """
    url = self._namespace_quota_url + "/" + name
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def add_namespace_user(self, namespace_user):
    """Add the namespace user.

    Args:
      namespace_user: The namespace user object to add.

    Returns:
      The dictionary of namespace user.
    """
    namespace_user_json = namespace_user.get_json_data()
    response = requests.post(self._namespace_user_url,
                             auth=self._auth,
                             data=namespace_user_json)
    return self.process_response(response, 'data')

  def remove_namespace_user(self, namespace_user):
    """Remove the namespace user.

    Args:
      namespace_user: The namespace user object to remove.

    Returns:
      The dictionary of namespace user.
    """
    namespace_user_json = namespace_user.get_json_data()
    response = requests.delete(self._namespace_user_url,
                               auth=self._auth,
                               data=namespace_user_json)
    return self.process_response(response)

  def list_namespace_users(self, namespace):
    """List namespace users.

    Returns:
      The list of dictionary of namespace quota.
    """
    url = self._namespace_user_url
    if namespace:
      url = url + "?namespace=" + namespace
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  def get_frameworks(self):
    response = requests.get(self._framework_url)
    return self.process_response(response)

  def authentication(self):
    response = requests.get(self._quota_url, auth=self._auth)
    if response.ok:
      return {"message": "Successfully verify aksk and Cloud-ML endpoint."}
    else:
      return {"error": True, "message": "Authentication failed."}

  def get_org_id(self):
    response = requests.get(self._org_id_url, auth=self._auth)
    return self.process_response(response)

  def list_cluster_resources(self, org_id=None):
    if org_id:
      url = self._resources_url + "?org_id=" + org_id
    else:
      url = self._resources_url
    response = requests.get(url, auth=self._auth)
    return self.process_response(response, 'data')

  @staticmethod
  def process_response(response, select_col_name=None):
    if response.ok:
      if select_col_name:
        return json.loads(response.content.decode("utf-8"))[select_col_name]
      else:
        return json.loads(response.content.decode("utf-8"))
    else:
      print("response: {}".format(response.content))
      sys.exit(1)
