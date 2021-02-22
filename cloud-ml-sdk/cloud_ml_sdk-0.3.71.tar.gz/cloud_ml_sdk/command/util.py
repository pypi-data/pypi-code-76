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
from datetime import datetime
import argparse
import base64
import fds
import getpass
import json
import logging
import copy
import os
import sys
import time

import requests
import yaml


sys.path.append("../../")

from . import color_util
from . import constant
from cloud_ml_sdk.client import CloudMlClient
from cloud_ml_sdk.models.train_job import TrainJob
from cloud_ml_sdk.models.model_service import ModelService
from cloud_ml_sdk.models.dev_env import DevEnv
from cloud_ml_sdk.models.tensorboard_service import TensorboardService
from cloud_ml_sdk.models.quota import Quota
from cloud_ml_sdk.models.dev_server import DevServer
from cloud_ml_sdk.models.pipeline import Pipeline
from cloud_ml_sdk.models.schedule import Schedule
from cloud_ml_sdk.models.ceph_service import CephService
from cloud_ml_sdk.models import models_util
from cloud_ml_sdk.models.secret_service import SecretService
from cloud_ml_sdk.models.namespace_service import NamespaceService
from cloud_ml_sdk.models.namespace_quota_service import NamespaceQuotaService
from cloud_ml_sdk.models.namespace_user_service import NamespaceUserService

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)


class SetConfigContextEnv(argparse.Action):
  def __call__(self, parser, namespace, values, option_string=None):
    # Set cloudml config context env
    os.environ['XIAOMI_CLOUDML_CONFIG_CONTEXT'] = values
    setattr(namespace, self.dest, values)


def compatibility_input(obj):
  if sys.version_info > (3, 0):
    res = input(obj)
  else:
    res = raw_input(obj)
  return res


def authentication(access_key, secret_key, endpoint, org_mail):
  client = CloudMlClient(access_key=access_key, secret_key=secret_key, endpoint=endpoint, xiaomi_org_mail=org_mail)
  response = client.authentication()
  if "error" in response:
    return False
  else:
    return True


def deprecated_init_config(args):
  """Deprecated cloudml init."""
  print("WARN: `cloudml init` has beed deprecated, please use `cloudml config init` instead.")
  print("We use a new sub-commands group for cloudml config now, including `init`, `show` and more.")
  print("You could get more details about the new config commands by `cloudml config -h`.")
  return


def init_fds(config_data=None):
  """Init fds related config.

  Returns:
    Dict of config_data.
  """
  if not config_data:
    config_data = {}
  access_key = None
  secret_key = None
  if config_data and "xiaomi_access_key_id" in config_data and "xiaomi_secret_access_key" in config_data:
    if compatibility_input("Use current AccessKey Pairs {}? [y/N]: ".format(
        config_data["xiaomi_access_key_id"])) in ["y", "Y"]:
      access_key = config_data["xiaomi_access_key_id"]
      secret_key = config_data["xiaomi_secret_access_key"]
  if not access_key and not secret_key:
    access_key = compatibility_input("\nPlease input access key: ")
    secret_key = getpass.getpass(
      "Please input secret key (will not be echoed): ")
    if access_key.find("/") >= 0 or secret_key.find("/") >= 0:
      print(color_util.colorize_warning("\nATTENSION:"))
      print(color_util.colorize_warning(
        "The access key and secret key with slashes may cause fault in getting data from fds when use tensorflow framework!\n"))

  print("\n[FDS CONFIG]")
  print("/ *")
  print("  * ----only for Xiaomi inner users----")
  print("  * {}".format(color_util.colorize_warning("Ecology cloud users can skip this steps")))
  print("  * c3 endpoint ({}): cnbj1-fds.api.xiaomi.net".format(color_util.colorize_warning("highly recommend")))
  print("  * wuqing endpoint: cnbj2m-fds.api.xiaomi.net")
  print("  * c3-inner endpoint: cnbj1-inner-fds.api.xiaomi.net")
  print("  */")
  fds_endpoint = compatibility_input("Please input fds endpoint: ")

  if access_key:
    config_data["xiaomi_access_key_id"] = access_key
  if secret_key:
    config_data["xiaomi_secret_access_key"] = secret_key
  if fds_endpoint:
    config_data["xiaomi_fds_endpoint"] = fds_endpoint

  return config_data


def init_hdfs(config_data=None):
  """Init hdfs related config.

  Returns:
    Dict of config_data.
  """
  if not config_data:
    config_data = {}
  hdfs_krb_account = None
  hdfs_krb_password = None
  hdfs_endpoint = None
  if config_data and "xiaomi_hdfs_krb_account" in config_data and "xiaomi_hdfs_krb_password" in config_data:
    if compatibility_input("Use current krb account/password Pairs {}? [y/N]: ".format(
        config_data["xiaomi_hdfs_krb_account"])) in ["y", "Y"]:
      hdfs_krb_account = config_data["xiaomi_hdfs_krb_account"]
      hdfs_krb_password = config_data["xiaomi_hdfs_krb_password"]
  if not hdfs_krb_account and not hdfs_krb_password:
    print("\n[HDFS CONFIG]")
    print("/*")
    print("  * ----only for Xiaomi inner users----")
    print("  * If you don't want set, you can skip this steps")
    print("  * Please make sure you have quota from https://kdc.d.xiaomi.net/hdfs_quota/hadoop/")
    print("  */")
    hdfs_krb_account = compatibility_input("Please input kerberos account: ")
    hdfs_krb_password = getpass.getpass("Please input kerberos password (will not be echoed): ")

  hdfs_endpoint = compatibility_input("Please input hdfs endpoint: ")

  if hdfs_krb_account:
    config_data["xiaomi_hdfs_krb_account"] = hdfs_krb_account
  if hdfs_krb_password:
    config_data["xiaomi_hdfs_krb_password"] = hdfs_krb_password
  if hdfs_endpoint:
    config_data["xiaomi_hdfs_endpoint"] = hdfs_endpoint

  return config_data


def init_cloudml(config_data=None):
  """Init cloudml related config.

  Returns:
    Dict of cloudml_config.
  """
  cloudml_config = {}

  xiaomi_org_mail = None
  if config_data and "xiaomi_org_mail" in config_data:
    if compatibility_input("Use current org mail {}? [y/N]: ".format(
        config_data["xiaomi_org_mail"])) in ["y", "Y"]:
      xiaomi_org_mail = config_data["xiaomi_org_mail"]
  if not xiaomi_org_mail:
    xiaomi_org_mail = compatibility_input("Please input xiaomi org mail: ")

  access_key = None
  secret_key = None
  if config_data and "xiaomi_access_key_id" in config_data and "xiaomi_secret_access_key" in config_data:
    if compatibility_input("Use current AccessKey Pairs {}? [y/N]: ".format(
        config_data["xiaomi_access_key_id"])) in ["y", "Y"]:
      access_key = config_data["xiaomi_access_key_id"]
      secret_key = config_data["xiaomi_secret_access_key"]
  if not access_key and not secret_key:
    access_key = compatibility_input("\nPlease input access key: ")
    secret_key = getpass.getpass(
      "Please input secret key (will not be echoed): ")
    if access_key.find("/") >= 0 or secret_key.find("/") >= 0:
      print(color_util.colorize_warning("\nATTENSION:"))
      print(color_util.colorize_warning(
        "The access key and secret key with slashes may cause fault in getting data from fds when use tensorflow framework!\n"))

  print("\n[Cloud-ML CONFIG]")
  print("/ *")
  print("  * ----for Xiaomi inner users----")
  print("  * c4 endpoint ({}): cnbj3-cloud-ml.api.xiaomi.net".format(color_util.colorize_warning("no GPU")))
  print("  * wuqing endpoint ({}): cnbj2-cloud-ml.api.xiaomi.net".format(color_util.colorize_warning("many GPUs")))
  print("  * ----for Ecology cloud users----")
  print("  * wuqing endpoint ({}): cnbj2.cloudml.api.xiaomi.com".format(color_util.colorize_warning("cpus and GPUs")))
  print("  */")
  cloudml_endpoint = compatibility_input("Please input cloudml endpoint: ")

  fds_bucket = None
  if config_data and "cloudml_default_fds_bucket" in config_data:
    if compatibility_input("Use current fds bucket {}? [y/N]: ".format(
        config_data["cloudml_default_fds_bucket"])) in ["y", "Y"]:
      fds_bucket = config_data["cloudml_default_fds_bucket"]
  if not fds_bucket:
    fds_bucket = compatibility_input(
      "Please input fds bucket name (which will be mounted on path '/fds' in Cloud-ML): ")

  cloudml_config["xiaomi_cloudml_endpoint"] = cloudml_endpoint
  if xiaomi_org_mail:
    cloudml_config["xiaomi_org_mail"] = xiaomi_org_mail
  if access_key:
    cloudml_config["xiaomi_access_key_id"] = access_key
  if secret_key:
    cloudml_config["xiaomi_secret_access_key"] = secret_key
  if fds_bucket:
    cloudml_config["cloudml_default_fds_bucket"] = fds_bucket

  return cloudml_config


def init_config_data(config_context_name):
  """Init cluster config.

  Returns:
    Dict of cluster_config.
  """
  config_data = {}

  config_data.update(init_fds())
  config_data.update(init_hdfs())

  config_data[constant.CLOUDML_CONFIG_KEY] = {
    config_context_name: init_cloudml(config_data)
  }

  need_re_config = False
  while True:
    if need_re_config:
      config_data[constant.CLOUDML_CONFIG_KEY] = {
        config_context_name: init_cloudml(config_data)
      }
    print("\n[Test CloudML Access]")
    if compatibility_input("Test access with supplied credentials? [y/N]: ") in ["y", "Y"]:
      if not authentication(config_data["xiaomi_access_key_id"],
                            config_data["xiaomi_secret_access_key"],
                            config_data[constant.CLOUDML_CONFIG_KEY][config_context_name]["xiaomi_cloudml_endpoint"],
                            config_data[constant.CLOUDML_CONFIG_KEY][config_context_name]["xiaomi_org_mail"]):
        print("ERROR: Cloud-ML test failed, invalid config message.")
        need_re_config = True
      else:
        print("Test successfully!")
        break
      if not compatibility_input("\nRetry configuration? [y/N]: ") in ["y", "Y"]:
        break
    else:
      break

  need_re_config = False
  while True:
    if need_re_config:
      config_data.update(init_fds())
    print("\n[Test FDS Access]")
    if compatibility_input("Test access with supplied credentials? [y/N]: ") in ["y", "Y"]:
      fds_endpoint = None
      fds_bucket = None
      if "xiaomi_fds_endpoint" in config_data:
        fds_endpoint = config_data["xiaomi_fds_endpoint"]
      if "cloudml_default_fds_bucket" in config_data:
        fds_bucket = config_data["cloudml_default_fds_bucket"]
      if constant.CLOUDML_CONFIG_KEY in config_data and config_context_name in config_data[constant.CLOUDML_CONFIG_KEY]:
        if "cloudml_default_fds_bucket" in config_data[constant.CLOUDML_CONFIG_KEY][config_context_name]:
          fds_bucket = config_data[constant.CLOUDML_CONFIG_KEY][config_context_name]["cloudml_default_fds_bucket"]
      if fds_endpoint and fds_bucket:
        try:
          fds_config = fds.FDSClientConfiguration()
          fds_config.set_endpoint(fds_endpoint)
          fds_client = fds.GalaxyFDSClient(
              config_data["xiaomi_access_key_id"],
              config_data["xiaomi_secret_access_key"],
              fds_config)
        except Exception as e:
          print("ERROR: Init FDS client failed: {}".format(e))
        else:
          if not fds_client.does_bucket_exist(fds_bucket):
            print("ERROR: FDS test failed, does bucket '{}' already created?".format(fds_bucket))
          else:
            print("Test successfully!")
            break
      else:
        print("ERROR: Cloud-ML test failed: Both xiaomi_fds_endpoint and cloudml_default_fds_bucket are needed.")
        need_re_config = True
      if not compatibility_input("\nRetry configuration? [y/N]: ") in ["y", "Y"]:
        break
    else:
      break

  return config_data


def init_config(args):
  """Set the initial config."""

  config_dir = os.path.join(os.path.expanduser("~"), constant.CONFIG_PATH)
  config_path = os.path.join(config_dir, constant.CONFIG_FILENAME)

  config_context_name = compatibility_input("Please name your cloudml config context: (e.g. wq, c4, GPU, CPU etc.) ")

  if config_context_name == constant.DEFAULT_CONFIG_CONTEXT:
    exit_as_error("{} is reserved for default config contest, please chose another name.".format(config_context_name))
    return

  modified = False

  config_data = {}
  if os.path.exists(config_path):
    try:
      with open(config_path) as data_file:
        config_data = json.load(data_file)
    except Exception as e:
      print(
          "{} already exists. But failed to load config file, exception: {}".format(
              config_path, e))
      exit_as_error("You need to fix the config file by hand.")
      return
    if "xiaomi_cloudml_endpoint" in config_data:
      # non-multi cluster config found, ask user to reuse it or not
      print("Non-multi cluster config found in file {} with content:".format(config_path))
      print_masked_sensitive(config_data)
      if constant.CLOUDML_CONFIG_KEY in config_data and "xiaomi_cloudml_endpoint" in config_data[constant.CLOUDML_CONFIG_KEY]:
        print(
          "Found 'xiaomi_cloudml_endpoint' and 'xiaomi_cloudml' same time.")
        print("Will ignore the 'xiaomi_cloudml_endpoint' settings.")
        del config_data["xiaomi_cloudml_endpoint"]
        # del config_data["xiaomi_org_mail"]
        # del config_data["cloudml_default_fds_bucket"]
      else:
        # non-multi cluster config found, ask user to reuse it or not
        if compatibility_input("Do you want to init {} with it? [y/N]: ".format(config_context_name)) in ["y", "Y"]:
          cluster_config = copy.deepcopy(config_data)
          del cluster_config["xiaomi_access_key_id"]
          del cluster_config["xiaomi_secret_access_key"]
          del cluster_config["xiaomi_fds_endpoint"]

          config_data[constant.CLOUDML_CONFIG_KEY] = {
            config_context_name: cluster_config
          }
          del config_data["xiaomi_cloudml_endpoint"]
          del config_data["xiaomi_org_mail"]
          del config_data["cloudml_default_fds_bucket"]
          modified = True
        else:
          # non-multi cluster config found, but not used, init new
          cluster_config = init_cloudml(config_data)
          config_data[constant.CLOUDML_CONFIG_KEY] = {
            config_context_name: cluster_config
          }
          modified = True
    else:
      if constant.CLOUDML_CONFIG_KEY in config_data:
        if config_context_name in config_data[constant.CLOUDML_CONFIG_KEY]:
          # target cluster already in cloudml_config, ask user to reset it
          print("{} cluster config found in file {}:".format(config_context_name, config_path))
          print(json.dumps(config_data[constant.CLOUDML_CONFIG_KEY][config_context_name], indent=4, sort_keys=True))
          if compatibility_input("Do you want to re-init it? [y/N]: ".format(config_context_name)) in ["y", "Y"]:
            cluster_config = init_cloudml(config_data)
            config_data[constant.CLOUDML_CONFIG_KEY][config_context_name] = cluster_config
            modified = True
        else:
          # target cluster config not found, init it with default config_data
          current_config = copy.copy(config_data)
          if constant.DEFAULT_CONFIG_CONTEXT in config_data[constant.CLOUDML_CONFIG_KEY]:
            default_cluster = config_data[constant.CLOUDML_CONFIG_KEY][constant.DEFAULT_CONFIG_CONTEXT]
            current_config.update(config_data[constant.CLOUDML_CONFIG_KEY][default_cluster])
          cluster_config = init_cloudml(current_config)
          config_data[constant.CLOUDML_CONFIG_KEY][config_context_name] = cluster_config
          modified = True
      else:
        # both 'xiaomi_cloudml_endpoint' and 'xiaomi_cloudml' not found
        # re-init whole config
        config_data = init_config_data(config_context_name)
        modified = True
  else:
    # config file not found, init whole config
    config_data = init_config_data(config_context_name)
    modified = True

  if modified:
    if constant.CLOUDML_CONFIG_KEY in config_data:
      if compatibility_input("Set current cluster as default? [y/N]: ") in ["y", "Y"]:
        config_data[constant.CLOUDML_CONFIG_KEY][constant.DEFAULT_CONFIG_CONTEXT] = config_context_name
      # check default_cluster has been set
      if (len(config_data[constant.CLOUDML_CONFIG_KEY]) > 1 and
          constant.DEFAULT_CONFIG_CONTEXT not in config_data[constant.CLOUDML_CONFIG_KEY]):
        while True:
          print("Multi cluster found but not set the default one.")
          cluster_list = [item for item in config_data[constant.CLOUDML_CONFIG_KEY]]
          default_cluster = compatibility_input("Set default cluster to {}: ".format(cluster_list))
          if default_cluster in cluster_list:
            config_data[constant.CLOUDML_CONFIG_KEY][constant.DEFAULT_CONFIG_CONTEXT] = default_cluster
            break
          else:
            print("Invalid config_context_name, please chose one from: {}".format(cluster_list))
          if compatibility_input("Skip settings? [y/N]: ") in ["y", "Y"]:
            print("Configuration aborted. Changes were NOT saved.")
            return
    else:
      exit_as_error("Invalid configuration: 'xiaomi_cloudml' not found. Please run 'cloudml config init' again.")
      return
    print("\n[Save]")
    if compatibility_input("Save settings? [y/N]: ") in ["y", "Y"]:
      if not os.path.exists(config_dir):
        os.makedirs(config_dir)
      with open(config_path, "w") as outfile:
        json.dump(config_data, outfile, indent=4)
      print("Configuration content:")
      print_masked_sensitive(config_data)
      print("Successfully initialize config file in path: {}".format(
          config_path))
    else:
      exit_as_error("Configuration aborted. Changes were NOT saved.")
      return
  else:
    print("cloudml config init operation exit without any modification.")


def fds_config(args):
  """Set the fds config."""
  config_dir = os.path.join(os.path.expanduser("~"), constant.CONFIG_PATH)
  config_path = os.path.join(config_dir, constant.CONFIG_FILENAME)

  modified = False

  config_data = {}
  if os.path.exists(config_path):
    try:
      with open(config_path) as data_file:
        config_data = json.load(data_file)
    except Exception as e:
      print("{} already exists. But failed to load config file, exception: {}"
          .format(config_path, e))
      exit_as_error("You need to fix the config file by hand.")
      return
    if "xiaomi_fds_endpoint" in config_data and "xiaomi_access_key_id" in config_data:
      # fds config found
      if compatibility_input("Use FDS endpoint/AccessKey other than {}/{}? [y/N]: ".format(
          config_data["xiaomi_fds_endpoint"], config_data["xiaomi_access_key_id"])) in ["y", "Y"]:
        config_data.update(init_fds(config_data))
        modified = True
    else:
      config_data.update(init_fds())
      modified = True
  else:
    # config file not found, need to run init
    exit_as_error("Config file not found. Please run 'cloudml config init' first.")
    return

  if modified:
    print("\n[Save]")
    if compatibility_input("Save settings? [y/N]: ") in ["y", "Y"]:
      if not os.path.exists(config_dir):
        os.makedirs(config_dir)
      with open(config_path, "w") as outfile:
        json.dump(config_data, outfile, indent=4)
      print("Configuration content:")
      print_masked_sensitive(config_data)
      print("Successfully initialize config file in path: {}".format(
          config_path))
    else:
      print("Configuration aborted. Changes were NOT saved.")
      return
  else:
    print("cloudml config fds operation exit without any modification.")


def hdfs_config(args):
  """Set the hdfs config."""
  config_dir = os.path.join(os.path.expanduser("~"), constant.CONFIG_PATH)
  config_path = os.path.join(config_dir, constant.CONFIG_FILENAME)

  modified = False

  config_data = {}
  if os.path.exists(config_path):
    try:
      with open(config_path) as data_file:
        config_data = json.load(data_file)
    except Exception as e:
      print(
          "{} already exists. But failed to load config file, exception: {}".format(
              config_path, e))
      print("You need to fix the config file by hand.")
      return
    if "xiaomi_hdfs_endpoint" in config_data and "xiaomi_hdfs_krb_account" in config_data:
      if compatibility_input("Use HDFS endpoint/Account other than {}/{}? [y/N]: ".format(
          config_data["xiaomi_hdfs_endpoint"], config_data["xiaomi_hdfs_krb_account"])) in ["y", "Y"]:
        config_data.update(init_hdfs(config_data))
        modified = True
    else:
      config_data.update(init_hdfs())
      modified = True
  else:
    # config file not found, need to run init
    exit_as_error("Config file not found. Please run 'cloudml config init' first.")
    return

  if modified:
    print("\n[Save]")
    if compatibility_input("Save settings? [y/N]: ") in ["y", "Y"]:
      if not os.path.exists(config_dir):
        os.makedirs(config_dir)
      with open(config_path, "w") as outfile:
        json.dump(config_data, outfile, indent=4)
      print("Configuration content:")
      print_masked_sensitive(config_data)
      print("Successfully initialize config file in path: {}".format(
          config_path))
    else:
      print("Configuration aborted. Changes were NOT saved.")
      return
  else:
    print("cloudml config hdfs operation exit without any modification.")


def show_config(args):
  """Show cloudml config."""

  config_dir = os.path.join(os.path.expanduser("~"), constant.CONFIG_PATH)
  config_path = os.path.join(config_dir, constant.CONFIG_FILENAME)

  config_data = {}
  if not os.path.exists(config_path):
    print("cloudml config file({}) not exists, please init one by: cloudml config init".format(config_path))
    return
  else:
    try:
      with open(config_path) as data_file:
        config_data = json.load(data_file)
    except Exception as e:
      print(
          "Failed to load config file {}, exception: {}".format(
              config_path, e))
      print("You need to fix the config file by hand.")
      return
  print_masked_sensitive(config_data)


def print_masked_sensitive(config):
  """Mask sensitive info in config data"""
  config_copy = copy.deepcopy(config)
  sensitive_keys = [
    "xiaomi_secret_access_key",
    "xiaomi_hdfs_krb_password",
  ]
  for key in sensitive_keys:
    if key in config_copy:
      config_copy[key] = "*" * 16
  if constant.CLOUDML_CONFIG_KEY in config_copy:
    for k,v in config_copy[constant.CLOUDML_CONFIG_KEY].items():
      for key in sensitive_keys:
        if key in v:
          config_copy[constant.CLOUDML_CONFIG_KEY][k][key] = "*" * 16

  print(json.dumps(config_copy, indent=4, sort_keys=True))


def set_default_config(args):
  """Set default cloudml config."""

  config_dir = os.path.join(os.path.expanduser("~"), constant.CONFIG_PATH)
  config_path = os.path.join(config_dir, constant.CONFIG_FILENAME)

  config_data = {}
  if not os.path.exists(config_path):
    print("cloudml config file({}) not exists, please init one by: cloudml config init".format(config_path))
    return
  else:
    try:
      with open(config_path) as data_file:
        config_data = json.load(data_file)
    except Exception as e:
      print(
          "Failed to load config file {}, exception: {}".format(
              config_path, e))
      print("You need to fix the config file by hand.")
      return
    if "xiaomi_cloudml_endpoint" in config_data:
      # non-multi context config found, ask user to run cloudml config init first.
      print("Non-multi context config found in file {}, please re-init by: cloudml config init".format(config_path))
      return
    else:
      if constant.CLOUDML_CONFIG_KEY in config_data:
        # verify target context key in config, if so set default_config_context else print error msg
        if args.config_context_name in config_data[constant.CLOUDML_CONFIG_KEY]:
          config_data[constant.CLOUDML_CONFIG_KEY][constant.DEFAULT_CONFIG_CONTEXT] = args.config_context_name
          with open(config_path, "w") as outfile:
            json.dump(config_data, outfile, indent=4)
          print("Successfully set default config context to: {}".format(
              args.config_context_name))
        else:
          print("Failed to set default config context to {}, it's not in the config file {}".format(
                args.config_context_name, config_path))
          print("Please chose valid config context name from the result of `cloudml config show`.")
          print("Or you can init an new config context config by: `cloudml config init`.")
      else:
        # no multi context config found, ask user to run cloudml config init first.
        print("No multi context config found in file {}, please re-init by: cloudml config init".format(config_path))
        return


def delete_config_context(args):
  """Delete cloudml config context."""

  config_dir = os.path.join(os.path.expanduser("~"), constant.CONFIG_PATH)
  config_path = os.path.join(config_dir, constant.CONFIG_FILENAME)

  config_data = {}
  if not os.path.exists(config_path):
    print("cloudml config file({}) not exists, please init one by: cloudml config init".format(config_path))
    return
  else:
    try:
      with open(config_path) as data_file:
        config_data = json.load(data_file)
    except Exception as e:
      print((
          "Failed to load config file {}, exception: {}".format(
              config_path, e)))
      print("You need to fix the config file by hand.")
      return
    if "xiaomi_cloudml_endpoint" in config_data:
      # non-multi context config found
      print("Non-multi context config found in file {} with content:".format(config_path))
      print((json.dumps(config_data, indent=4, sort_keys=True)))
      print("Please re-init it to support multi context config commands by: cloudml config init")
      return
    else:
      if constant.CLOUDML_CONFIG_KEY in config_data:
        modified = False
        for config_context_name in args.config_context_names:
          # delete default config context is not allowed
          if config_context_name == config_data[constant.CLOUDML_CONFIG_KEY][constant.DEFAULT_CONFIG_CONTEXT]:
            print("{} is your defalut config context, it's not allow to delete.".format(config_context_name))
            print("Please change your default context first by: cloudml config set_default <name_of_other_context>")
            return
          # verify target context names in config, if so delete it else print error msg
          if config_context_name in config_data[constant.CLOUDML_CONFIG_KEY]:
            del config_data[constant.CLOUDML_CONFIG_KEY][config_context_name]
            modified = True
            print("Successfully deleted config context: {}".format(config_context_name))
          else:
            print("Failed to delete config context {}, it's not in the config file {}".format(
                config_context_name, config_path))
        if modified:
          with open(config_path, "w") as outfile:
            json.dump(config_data, outfile, indent=4)
      else:
        # no multi context config found, ask user to run cloudml config init first.
        print("No multi context config found in file {}, please re-init by: cloudml config init".format(config_path))
        return


def get_org_id(args):
  """Get org_id by access_key and secret_key in config file."""

  try:
    client = CloudMlClient()
  except Exception as e:
    print("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  response = client.get_org_id()
  if isinstance(response, str):
    print("response: {}".format(response))
  else:
    print("Your org_id is: {}".format(response.get("org_id")))

def print_hp_job_info(hp_job):
  """Print hp job in customed format.

    Args:
      hp_job: The dictionary of response hptuning job data.
    """
  if "message" in hp_job:
    print((hp_job["message"]))
  print("{:16} {}".format("Org id:", hp_job["org_id"]))
  print("{:16} {}".format("Org name:", hp_job["org_name"]))
  print("{:16} {}".format("hp name:", hp_job["hp_name"]))
  print("{:16} {}".format("Module name:", hp_job["module_name"]))
  print("{:16} {}".format("Trainer uri:", hp_job["trainer_uri"]))
  print("{:16} {}".format("Job args:", hp_job["job_args"]))
  print("{:16} {}".format("FDS Endpoint:", hp_job["fds_endpoint"]))
  print("{:16} {}".format("Fuse mount bucket:", hp_job["fds_bucket"]))
  print("{:16} {}".format("Kerberos account:", hp_job["hdfs_krb_account"]))
  print("{:16} {}".format("HDFS Endpoint:", hp_job["hdfs_endpoint"]))
  print("{:16} {}".format("CPU limit:", hp_job["cpu_limit"]))
  print("{:16} {}".format("Memory limit:", hp_job["memory_limit"]))
  print("{:16} {}".format("GPU limit:", hp_job["gpu_limit"]))
  print("{:16} {}".format("Current rank", hp_job.get("current_rank","-")))
  print("{:16} {}".format("Docker image:", hp_job["docker_image"]))
  print("{:16} {}".format("Docker command:", hp_job["docker_command"]))
  print("{:16} {}".format("Framework:", hp_job["framework"]))
  print("{:16} {}".format("Framework version:", hp_job[
      "framework_version"]))
  print("{:16} {}".format("State:", color_util.colorize_state(hp_job["state"])))
  print("{:16} {}".format("Create time:", hp_job["create_time"]))
  print("{:16} {}".format("Update time:", hp_job["update_time"]))

  print("{:16} {}".format("Volume type:", hp_job["volume_type"]))
  print("{:16} {}".format("Volume path:", hp_job["volume_path"]))
  print("{:16} {}".format("Mount path:", hp_job["mount_path"]))
  print("{:16} {}".format("Mount read only:", hp_job["mount_read_only"]))
  print("{:16} {}".format("Prepare command:", hp_job["prepare_command"]))
  print("{:16} {}".format("Finish command:", hp_job["finish_command"]))
  if "node_selector" in hp_job and hp_job["node_selector"]:
    print("{:16} {}".format("Node selector:", hp_job["node_selector"]))
  print("{:16} {}".format("Monitoring url:", hp_job["monitoring"] if "monitoring" in hp_job else ""))
  print("{:16} {}".format("Owner:", hp_job["owner"]))
  print("{:16} {}".format("Optimization type:", hp_job["optimization_type"]))
  print("{:16} {}".format("Objectivevalue name:", hp_job["objectivevalue_name"]))
  print("{:16} {}".format("Metrics names:", hp_job["metrics_names"]))
  print("{:16} {}".format("Parameter configs:", hp_job["parametertype_configs"]))
  print("{:16} {}".format("Suggestion algorithm:", hp_job["suggestion_algorithm"]))
  print("{:16} {}".format("Request number:", hp_job["request_number"]))

def print_train_job_info(train_job):
  """Print train job in customed format.

  Args:
    train_job: The dictionary of response train job data.
  """
  if "message" in train_job:
    print((train_job["message"]))
  print("{:16} {}".format("Org id:", train_job["org_id"]))
  print("{:16} {}".format("Org name:", train_job["org_name"]))
  print("{:16} {}".format("Job name:", train_job["job_name"]))
  print("{:16} {}".format("Module name:", train_job["module_name"]))
  print("{:16} {}".format("Trainer uri:", train_job["trainer_uri"]))
  print("{:16} {}".format("Job args:", train_job["job_args"]))
  print("{:16} {}".format("FDS Endpoint:", train_job["fds_endpoint"]))
  print("{:16} {}".format("Fuse mount bucket:", train_job["fds_bucket"]))
  print("{:16} {}".format("Kerberos account:", train_job["hdfs_krb_account"]))
  print("{:16} {}".format("HDFS Endpoint:", train_job["hdfs_endpoint"]))
  print("{:16} {}".format("CPU limit:", train_job["cpu_limit"]))
  print("{:16} {}".format("Memory limit:", train_job["memory_limit"]))
  print("{:16} {}".format("GPU limit:", train_job["gpu_limit"]))
  print("{:16} {}".format("Current rank", train_job.get("current_rank","-")))
  print("{:16} {}".format("Docker image:", train_job["docker_image"]))
  print("{:16} {}".format("Docker command:", train_job["docker_command"]))
  print("{:16} {}".format("Framework:", train_job["framework"]))
  print("{:16} {}".format("Framework version:", train_job[
      "framework_version"]))
  print("{:16} {}".format("State:", color_util.colorize_state(train_job["state"])))
  print("{:16} {}".format("Create time:", train_job["create_time"]))
  print("{:16} {}".format("Update time:", train_job["update_time"]))
  if train_job["cluster_name"]:
    print("{:16} {}".format("Cluster name:", train_job["cluster_name"]))
  if train_job["service_port"]:
    print("{:16} {}".format("Service port:", train_job["service_port"]))
  if train_job["cluster_env_var"]:
    print("{:16} {}".format("Cluter environment variables:", train_job[
        "cluster_env_var"]))
  if train_job["hyperparameters_name"]:
    print("{:16} {}".format("Hyperparameters name:", train_job[
        "hyperparameters_name"]))
  if train_job["hyperparameters_goal"]:
    print("{:16} {}".format("Hyperparameters goal:", train_job[
        "hyperparameters_goal"]))
  if train_job["hyperparameters_params"]:
    print("{:16} {}".format("Hyperparameters params:", train_job[
        "hyperparameters_params"]))
  print("{:16} {}".format("Volume type:", train_job["volume_type"]))
  print("{:16} {}".format("Volume path:", train_job["volume_path"]))
  print("{:16} {}".format("Mount path:", train_job["mount_path"]))
  print("{:16} {}".format("Mount read only:", train_job["mount_read_only"]))
  print("{:16} {}".format("Prepare command:", train_job["prepare_command"]))
  print("{:16} {}".format("Finish command:", train_job["finish_command"]))
  if "node_selector" in train_job and train_job["node_selector"]:
    print("{:16} {}".format("Node selector:", train_job["node_selector"]))
  if "node_name" in train_job and train_job["node_name"]:
    print("{:16} {}".format("Node name:", train_job["node_name"]))
  print("{:16} {}".format("Monitoring url:", train_job["monitoring"] if "monitoring" in train_job else ""))



def print_model_service_info(model):
  """Print model service in customed format.

  Args:
    model: The dictionary of response model service data.
  """
  print("{:16} {}".format("Org id:", model["org_id"]))
  print("{:16} {}".format("Org name:", model["org_name"]))
  print("{:16} {}".format("Model name:", model["model_name"]))
  print("{:16} {}".format("Model version:", model["model_version"]))
  print("{:16} {}".format("Model uri:", model["model_uri"]))
  print("{:16} {}".format("Model args:", model["model_args"]))
  print("{:16} {}".format("FDS Endpoint:", model["fds_endpoint"]))
  print("{:16} {}".format("Fuse mount bucket:", model["fds_bucket"]))
  if not model.get("use_seldon"):
    print("{:16} {}".format("Service port:", model["service_port"]))
  print("{:16} {}".format("Replicas:", model["replicas"]))
  print("{:16} {}".format("Pod Replicas:", model["pod_replicas"] if model.has_key("pod_replicas") else model["replicas"]))
  print("{:16} {}( x {})".format("CPU limit:", model["cpu_limit"], model[
      "replicas"]))
  print("{:16} {}( x {})".format("Memory limit:", model["memory_limit"], model[
      "replicas"]))
  print("{:16} {}( x {})".format("GPU limit:", model["gpu_limit"], model[
      "replicas"]))
  print("{:16} {}".format("Current rank:", model.get("current_rank","-")))
  print("{:16} {}".format("Docker image:", model["docker_image"]))
  if not model.get("use_seldon",None):
    print("{:16} {}".format("Docker command:", model["docker_command"]))
    print("{:16} {}".format("Framework:", model["framework"]))
    print("{:16} {}".format("Framework version:", model["framework_version"]))
  print("{:16} {}".format("State:", color_util.colorize_state(model["state"])))
  print("{:16} {}".format("Create time:", model["create_time"]))
  print("{:16} {}".format("Update time:", model["update_time"]))
  if model.get("http_address",None):
    print("{:16} {}".format("HTTP Address:", model["http_address"]))
  if model.get("use_seldon",None):
    print("{:16} {}".format("GRPC Address:", model["grpc_address"]))
    print("{:16} {}".format("HTTP Address:", model["rest_address"]))
    print("{:16} {}".format("Engine CPU limit:", model["engine_cpu_limit"]))
    print("{:16} {}".format("Engine Memory limit:", model["engine_memory_limit"]))
    print("{:16} {}".format("Oauth Token:", model["oauth_token"]))
    print("{:16} {}".format("Initial Delay Seconds:", model["initial_delay_seconds"]))
  if not model.get("use_seldon",None):
    print("{:16} {}".format("Prepare command:", model["prepare_command"]))
    print("{:16} {}".format("Finish command:", model["finish_command"]))
  if "node_selector" in model and model["node_selector"]:
    print("{:16} {}".format("Node selector:", model["node_selector"]))
  if model.get("use_seldon",None) and "monitoring" in model:
    monitoring = json.loads(model["monitoring"])
    print("{:16} {}".format("Engine Monitoring url:", monitoring["engine"][0] if monitoring["engine"] else ""))
    print("{:16} {}".format("Model Monitoring url:", monitoring["model"][0] if monitoring["model"] else ""))
  else:
    print("{:16} {}".format("Monitoring url:", model["monitoring"] if "monitoring" in model else ""))


def print_dev_env_info(dev_env):
  """Print dev_env in customed format.

  Args:
    dev_env: The dictionary of response dev env data.
  """
  print("{:16} {}".format("Org id:", dev_env["org_id"]))
  print("{:16} {}".format("Org name:", dev_env["org_name"]))
  print("{:16} {}".format("Dev name:", dev_env["dev_name"]))
  print("{:16} {}".format("Password:", dev_env["password"]))
  print("{:16} {}".format("Notebook port:", dev_env["notebook_port"]))
  print("{:16} {}".format("Ssh port:", dev_env["ssh_port"]))
  print("{:16} {}".format("FDS Endpoint:", dev_env["fds_endpoint"]))
  print("{:16} {}".format("Fuse mount bucket:", dev_env["fds_bucket"]))
  print("{:16} {}".format("Kerberos account:", dev_env["hdfs_krb_account"]))
  print("{:16} {}".format("HDFS Endpoint:", dev_env["hdfs_endpoint"]))
  print("{:16} {}".format("Ceph volume:", dev_env["ceph_volume"] if "ceph_volume" in dev_env else ""))
  print("{:16} {}".format("Ceph mode:", dev_env["ceph_mode"] if "ceph_mode" in dev_env else ""))
  print("{:16} {}".format("CPU limit:", dev_env["cpu_limit"]))
  print("{:16} {}".format("Memory limit:", dev_env["memory_limit"]))
  print("{:16} {}".format("GPU limit:", dev_env["gpu_limit"]))
  print("{:16} {}".format("Current rank:",dev_env.get("current_rank","-")))
  print("{:16} {}".format("Docker image:", dev_env["docker_image"]))
  print("{:16} {}".format("Docker command:", dev_env["docker_command"]))
  print("{:16} {}".format("Framework:", dev_env["framework"]))
  print("{:16} {}".format("Framework version:", dev_env["framework_version"]))
  print("{:16} {}".format("State:", color_util.colorize_state(dev_env["state"])))
  print("{:16} {}".format("Create time:", dev_env["create_time"]))
  print("{:16} {}".format("Update time:", dev_env["update_time"]))
  print("{:16} {}".format("Jupyter Address:", dev_env["address"]))
  print("{:16} {}".format("Ssh address:", dev_env["ssh_address"]))
  print("{:16} {}".format("Proxy whitelist:", dev_env["proxy_whitelist"]))
  if "node_selector" in dev_env and dev_env["node_selector"]:
    print("{:16} {}".format("Node selector:", dev_env["node_selector"]))
  print("{:16} {}".format("Monitoring url:", dev_env["monitoring"] if "monitoring" in dev_env else ""))
  print("{:16}".format("Networks:"))
  if "network" in dev_env:
      networks = dev_env["network"]
      for network in networks:
          print("{:16} {} {}/{}:{}".format("",
              network["address"],
              network["protocol"],
              network["port"],
              network["whitelist"]))

def print_dev_server_info(dev_server):
  """Print dev_server in customed format.

  Args:
    dev_server: The dictionary of response dev server data.
  """
  print("{:16} {}".format("Org id:", dev_server["org_id"]))
  print("{:16} {}".format("Org name:", dev_server["org_name"]))
  print("{:16} {}".format("Dev name:", dev_server["dev_name"]))
  print("{:16} {}".format("Password:", dev_server["password"]))
  print("{:16} {}".format("Notebook port:", dev_server["notebook_port"]))
  print("{:16} {}".format("Ssh port:", dev_server["ssh_port"]))
  print("{:16} {}".format("CPU limit:", dev_server["cpu_limit"]))
  print("{:16} {}".format("Memory limit:", dev_server["memory_limit"]))
  print("{:16} {}".format("GPU limit:", dev_server["gpu_limit"]))
  print("{:16} {}".format("Current rank:", dev_server.get("current_rank","-")))
  print("{:16} {}".format("Docker image:", dev_server["docker_image"]))
  print("{:16} {}".format("Docker command:", dev_server["docker_command"]))
  print("{:16} {}".format("Framework:", dev_server["framework"]))
  print("{:16} {}".format("Framework version:", dev_server[
      "framework_version"]))
  print("{:16} {}".format("State:", color_util.colorize_state(dev_server["state"])))
  print("{:16} {}".format("Create time:", dev_server["create_time"]))
  print("{:16} {}".format("Update time:", dev_server["update_time"]))
  print("{:16} {}".format("Address:", dev_server["address"]))
  print("{:16} {}".format("Ssh address:", dev_server["ssh_address"]))


def print_tensorboard_info(tensorboard):
  """Print tensorboard in customed format.

  Args:
    tensorboard: The dictionary of response tensorboard data.
  """
  print("{:16} {}".format("Org id:", tensorboard["org_id"]))
  print("{:16} {}".format("Org name:", tensorboard["org_name"]))
  print("{:16} {}".format("Tensorboard name:", tensorboard["tensorboard_name"]))
  print("{:16} {}".format("Logdir:", tensorboard["logdir"]))
  print("{:16} {}".format("Current rank:", tensorboard.get("current_rank", "-")))
  print("{:16} {}".format("Service port:", tensorboard["service_port"]))
  print("{:16} {}".format("Docker image:", tensorboard["docker_image"]))
  print("{:16} {}".format("Docker command:", tensorboard["docker_command"]))
  print("{:16} {}".format("Framework:", tensorboard["framework"]))
  print("{:16} {}".format("Framework version:", tensorboard["framework_version"]))
  print("{:16} {}".format("State:", color_util.colorize_state(tensorboard["state"])))
  print("{:16} {}".format("Create time:", tensorboard["create_time"]))
  print("{:16} {}".format("Update time:", tensorboard["update_time"]))
  print("{:16} {}".format("Address:", tensorboard["address"]))
  if "node_selector" in tensorboard and tensorboard["node_selector"]:
    print("{:16} {}".format("Node selector:", tensorboard["node_selector"]))
  print("{:16} {}".format("FDS Endpoint:", tensorboard["fds_endpoint"]))
  print("{:16} {}".format("Fuse mount bucket:", tensorboard["fds_bucket"]))
  print("{:16} {}".format("Monitoring url:", tensorboard["monitoring"] if "monitoring" in tensorboard else ""))


def print_quota_info(quota):
  """Print quota in customed format.

  Args:
    quota: The dictionary of response quota data.
  """
  total_memory_quota = "INF" if quota[
      "total_memory_quota"] == constant.INF_TOTAL_MEMORY_QUOTA else quota[
          "total_memory_quota"]
  total_cpu_quota = "INF" if quota[
      "total_cpu_quota"] == constant.INF_TOTAL_CPU_QUOTA else quota[
          "total_cpu_quota"]
  total_gpu_quota = "INF" if quota[
      "total_gpu_quota"] == constant.INF_TOTAL_GPU_QUOTA else quota[
          "total_gpu_quota"]
  train_count_quota = "INF" if quota[
      "train_count_quota"] == constant.INF_JOB_COUNT else quota[
          "train_count_quota"]
  model_count_quota = "INF" if quota[
      "model_count_quota"] == constant.INF_JOB_COUNT else quota[
          "model_count_quota"]
  dev_count_quota = "INF" if quota[
      "dev_count_quota"] == constant.INF_JOB_COUNT else quota[
          "dev_count_quota"]

  print("{:16} {}".format("Org id:", quota["org_id"]))
  if "org_mail" in quota:
    print("{:16} {}".format("Org mail address:", quota["org_mail"]))
  print("{:16} {:26} {:26} {:26} {:26} {:26} {:26} {:26}".format(
      "",
      "Memory / Used",
      "CPU / Used",
      "GPU / Used",
      "Tensorboard / Used",
      "Current rank",
      "Priority / Used",
      "Count / Used"
      ))
  print("{:16} {:26} {:26} {:26} {:26} {:26} {:26} {:26}".format(
      "Train job",
      quota["train_memory_quota"] + " / " + quota["train_memory_used"],
      quota["train_cpu_quota"] + " / " + quota["train_cpu_used"],
      quota["train_gpu_quota"] + " / " + quota["train_gpu_used"],
      "- / -",
      quota.get("train_priority_rank","-"),
      quota.get("train_priority_quota", "-") + " / " + quota.get("train_priority_used", "-"),
      train_count_quota + " / " + quota["train_count_used"]
      ))
  print("{:16} {:26} {:26} {:26} {:26} {:26} {:26} {:26}".format(
      "Model service",
      quota["model_memory_quota"] + " / " + quota["model_memory_used"],
      quota["model_cpu_quota"] + " / " + quota["model_cpu_used"],
      quota["model_gpu_quota"] + " / " + quota["model_gpu_used"],
      "- / -",
      quota.get("model_priority_rank","-"),
      quota.get("model_priority_quota","-") + " / " + quota.get("model_priority_used","-"),
      model_count_quota + " / " + quota["model_count_used"]
      ))
  print("{:16} {:26} {:26} {:26} {:26} {:26} {:26} {:26}".format(
      "Dev environment",
      quota["dev_memory_quota"] + " / " + quota["dev_memory_used"],
      quota["dev_cpu_quota"] + " / " + quota["dev_cpu_used"],
      quota["dev_gpu_quota"] + " / " + quota["dev_gpu_used"],
      "- / -",
      quota.get("dev_priority_rank", "-"),
      quota.get("dev_priority_quota", "-") + " / " + quota.get("dev_priority_used", "-"),
      dev_count_quota + " / " + quota["dev_count_used"]
      ))
  print("{:16} {:26} {:26} {:26} {:26} {:26} {:26} {:26}".format(
      "Tensorboard",
      "- / -",
      "- / -",
      "- / -",
      quota["tensorboard_quota"] + " / " + quota["tensorboard_used"],
      quota.get("tensorboard_priority_rank", "-"),
      quota.get("tensorboard_priority_quota", "-") + " / " + quota.get("tensorboard_priority_used", "-"),
      "- / -"
      ))

  print("{:16} {:26} {:26} {:26} {:26} {:26} {:26} {:26}".format(
      "Total quota",
      total_memory_quota + " / " + quota["total_memory_used"],
      total_cpu_quota + " / " + quota["total_cpu_used"],
      total_gpu_quota + " / " + quota["total_gpu_used"],
      "- / -",
      "-",
      "- / -",
      "- / -"
      ))


def print_frameworks_info(framework):
  print("{:16} {}".format("FRAMEWORK", "FRAMEWORK"))
  for framework_name in framework:
    for index in range(len(framework[framework_name])):
      if index == 0:
        print("{:16} {}".format(framework_name, framework[framework_name][
            index]))
      else:
        print("{:16} {}".format("", framework[framework_name][index]))


def print_pipeline_info(response):
  """Print pipeline customed format.

  Args:
    pipeline: The dictionary of response train job data.
  """

  pipeline = response['data']
  if "message" in pipeline:
    print((pipeline["message"]))
  print("{:16} {}".format("Org id:", pipeline["org_id"]))
  print("{:16} {}".format("Org name:", pipeline["org_name"]))
  print("{:16} {}".format("Pipeline name:", pipeline["pipeline_name"]))
  print("{:16} {}".format("Pipeline config:", pipeline["pipeline_config"]))

  #print("{:16}{}".format("Pipeline argo yaml:\n", pipeline["argo_yaml"]))
  print("{:16} {}".format("FDS Endpoint:", pipeline["fds_endpoint"]))
  print("{:16} {}".format("Fuse mount bucket:", pipeline["fds_bucket"]))
  print("{:16} {}".format("Create time:", pipeline["create_time"]))
  print("{:16} {}".format("Update time:", pipeline["update_time"]))
  if "argo_get_success" in pipeline:
    print("#"*48)
    if pipeline["argo_get_success"]:
      print("ARGO INFO AS FOLLOWS")
      print("#"*48)
      print("{:16} {}".format("Argo UI:", pipeline["argo_ui"]))
    else:
      print("ARGO GET FAILED")
      print("#"*48)
    print(pipeline["argo_get_info"].encode("utf-8"))

  if 'error' in response and len(response["error"]) > 0:

    print("\nERROR MESSAGE")
    for pipeline_type in response['error']:
      print("{} error: {}".format(pipeline_type, response['error'][pipeline_type]))

def print_pipeline_schedule_info(response):
  pipeline_schedule = response['data']
  if "message" in pipeline_schedule:
    print((pipeline_schedle["message"]))
  print("{:16} {}".format("Org id:", pipeline_schedule["org_id"]))
  print("{:16} {}".format("Pipeline name:", pipeline_schedule["pipeline_name"]))
  print("{:16} {}".format("State:", pipeline_schedule["state"]))
  print("{:16} {}".format("Create time:", pipeline_schedule["create_time"]))
  print("{:16} {}".format("Update time:", pipeline_schedule["update_time"]))
  if "argo_get_success" in pipeline_schedule:
    print("#"*48)
    if pipeline_schedule["argo_get_success"]:
      print("ARGO INFO AS FOLLOWS")
      print("#"*48)
      print("{:16} {}".format("Argo UI:", pipeline_schedule["argo_ui"]))
    else:
      print("ARGO GET FAILED")
      print("#"*48)
    print(pipeline_schedule["argo_get_info"].encode("utf-8"))

  if 'error' in response and len(response["error"]) > 0:

    print("\nERROR MESSAGE")
    for pipeline_type in response['error']:
      print("{} error: {}".format(pipeline_type, response['error'][pipeline_type]))


def print_secret_info(secret):
  """Print secret in customed format.

  Args:
    secret: The dictionary of response secret data.
  """
  print("{:16} {}".format("Org id:", secret["org_id"]))
  print("{:16} {}".format("Org name:", secret["org_name"]))
  print("{:16} {}".format("secret name:", secret["secret_name"]))
  print("{:16} {}".format("Create time:", secret["create_time"]))
  #print("{:16} {}".format("Data:", secret["Data"]))


def print_predict_result(result):
  """Print the predict result in customed format.

  Args:
    result: The predict result. Example: {u"predict": [30.00011444091797, 70.00050354003906], u"keys": [10, 20]}
  """
  print("Predictions:")
  for i in range(len(list(result.values())[0])):
    print_divider = True
    for k, v in list(result.items()):
      if print_divider:
        print("{} {}: {}".format("-", k, v[i]))
        print_divider = False
      else:
        print("{} {}: {}".format(" ", k, v[i]))


def print_hyperparameter_data_result(result):
  """Print the hyperparameter result in customed format.

  Args:
    result: The result. Example: {"best_trials": {}, "goal": "MINIMIZE", "trialCount": 4, "trial": [{}]}
                                 Each trial contains {"metric": 0.08, "params": "--foo=bar", "step": 100}
  """
  print("Goal: {}".format(result["goal"]))
  print("Trial count: {}".format(result["trialCount"]))
  print("Best trial:")
  print("{:8} Metrics: {}".format("", result["best_trials"]["metric"]))
  print("{:8} Params: {}".format("", result["best_trials"]["params"]))
  print("{:8} Step: {}".format("", result["best_trials"]["step"]))
  print("{:8} State: {}".format("", result["best_trials"]["state"]))

  trials = result["trials"]
  for i in range(len(trials)):
    print("Trial {}:".format(i))
    print("{:8} Metrics: {}".format("", trials[i]["metric"]))
    print("{:8} Params: {}".format("", trials[i]["params"]))
    print("{:8} Step: {}".format("", trials[i]["step"]))
    print("{:8} State: {}".format("", trials[i]["state"]))


def print_kubernetes_events(events):
  """Print the events logs from Kubernetes API.

  Args:
    events: The list of event. Example: {"count": 1, "firstTimestamp": "2017-02-20T06:16:39Z"}
  """
  if isinstance(events,dict):
    print("engine events: ")
    print("{:20} {:20} {:8} {:32} {:8} {:8} {}".format(
        "FirstTimestamp", "LastTimestamp", "Count", "Name", "Type", "Reason",
        "Message"))
    if "engine" in events and len(events["engine"]) > 0:
      for event in events["engine"][0]:
        print("{:20} {:20} {:8} {:32} {:8} {:8} {}".format(event[
            "firstTimestamp"], event["lastTimestamp"], event["count"], event[
                "involvedObject"]["name"], event["type"], event["reason"], event[
                    "message"]))
    print("model events: ")
    print("{:20} {:20} {:8} {:32} {:8} {:8} {}".format(
        "FirstTimestamp", "LastTimestamp", "Count", "Name", "Type", "Reason",
        "Message"))
    if "model" in events and len(events["model"]) > 0:
      for event in events["model"][0]:
        print("{:20} {:20} {:8} {:32} {:8} {:8} {}".format(event[
            "firstTimestamp"], event["lastTimestamp"], event["count"], event[
                "involvedObject"]["name"], event["type"], event["reason"], event[
                    "message"]))

  else:
    print("{:20} {:20} {:8} {:32} {:8} {:8} {}".format(
        "FirstTimestamp", "LastTimestamp", "Count", "Name", "Type", "Reason",
        "Message"))
    for event in events:
      print("{:20} {:20} {:8} {:32} {:8} {:8} {}".format(event[
          "firstTimestamp"], event["lastTimestamp"], event["count"], event[
              "involvedObject"]["name"], event["type"], event["reason"], event[
                  "message"]))

def print_recommend_resource(resource):
  print("recommend resources configure:")
  print("{:32} {:32} {:32}".format("Available cpu", "Available memory", "Available gpu"))
  for item in resource:
    mem = round(float(item[1]) / 1000**3,3)
    print("{:32} {:32} {:32}".format(str(item[0]), str(mem)+"G", str(item[2])))


def print_metrics_result(metrics):
  """Print the metrics result.

  Args:
    metrics: The metrics.
  """
  print("{:20} {} %".format("CPU:", metrics["cpu"]))
  print("{:20} {} Bytes".format("Memory:", metrics["memory"]))
  print("{:20} {} Bytes".format("Network receive:", metrics["network_receive"]))
  print("{:20} {} Bytes".format("Network transmit:", metrics["network_transmit"]))

def list_jobs(args):
  """List train jobs."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      response_train_jobs = client.list_train_jobs(
          constant.CLOUDML_ALL_ORG_PARAMETER)
    else:
      response_train_jobs = client.list_train_jobs(args.org_id)
  else:
    response_train_jobs = client.list_train_jobs()
  if not isinstance(response_train_jobs, str):
    print_trainjob_list(response_train_jobs, args)
  else:
    print("response: {}".format(response_train_jobs))

def print_trainjob_list(response_train_jobs, args):
  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
     if "output" in args and args.output == "wide":
        print("{:16} {:16} {:32} {:16} {:32} {:32} {:32}".format(
           "ORG ID", "ORG NAME", "JOB_NAME", "STATE", "CREATED", "UPDATED", "NODE NAME"))
        for train_job in response_train_jobs:
           print("{:<16} {:16} {:32} {:16} {:32} {:32} {:32}".format(train_job[
                                                            "org_id"], train_job["org_name"], train_job["job_name"],
                                                          color_util.colorize_state(train_job["state"]),
                                                          train_job["create_time"], train_job["update_time"],
                                                          train_job["node_name"]))
     else:
        print("{:16} {:16} {:32} {:16} {:32} {:32}".format(
           "ORG ID", "ORG NAME", "JOB_NAME", "STATE", "CREATED", "UPDATED"))
        for train_job in response_train_jobs:
           print("{:<16} {:16} {:32} {:16} {:32} {:32}".format(train_job[
                                                            "org_id"], train_job["org_name"], train_job["job_name"],
                                                          color_util.colorize_state(train_job["state"]),
                                                          train_job["create_time"], train_job["update_time"]))
  else:
      if "output" in args and args.output == "wide":
          print("{:32} {:16} {:32} {:32} {:32}".format("JOB_NAME", "STATE", "CREATED", "UPDATED", "NODE NAME"))
          for train_job in response_train_jobs:
              print("{:32} {:16} {:32} {:32} {:32}".format(train_job[
                                                         "job_name"], color_util.colorize_state(train_job["state"]),
                                                     train_job["create_time"], train_job["update_time"],
                                                     train_job["node_name"]))
      else:
          print("{:32} {:16} {:32} {:32}".format("JOB_NAME", "STATE", "CREATED",
                                           "UPDATED"))
          for train_job in response_train_jobs:
              print("{:32} {:16} {:32} {:32}".format(train_job[
                                               "job_name"], color_util.colorize_state(train_job["state"]),
                                             train_job["create_time"], train_job["update_time"]))


def setNetwork():
  task_port_types = compatibility_input("Please input port, separated with a space. [Default is: {}]: ".format(
    " ".join(
      ["{}(for {})".format(x[0],x[1]) for x in list(constant.DEV_PROXY_PROTOCOL.items())]
      )
    )
  ) or list(constant.DEV_PROXY_PROTOCOL.keys())
  if not isinstance(task_port_types,list):
    port_list = task_port_types.strip().split(" ")
    port_list = [models_util.check_network_port(port) for port in port_list]
  else:
    port_list = task_port_types
  networkList = []
  jupyter_num = 0
  for i in port_list:
    netDict = {}
    netDict["port"] = i
    protocol = compatibility_input("\nPlease input the protocol of port:'{}'{}: ".
                                   format(i,". [Default is ]"+constant.DEV_PROXY_PROTOCOL[i] if constant.DEV_PROXY_PROTOCOL.get(i) else "")) \
               or constant.DEV_PROXY_PROTOCOL.get(i)
    if protocol not in list(constant.DEV_PROXY_PROTOCOL.values()):
      raise ValueError("Network protocol must be in {}".format(str(list(constant.DEV_PROXY_PROTOCOL.values()))))
    if protocol == "JUPYTER":
      jupyter_num += 1
    if jupyter_num > 1:
      raise ValueError("Multiple JUPYTER protocol is not allowed")
    netDict["protocol"] = protocol
    whitelist = compatibility_input(
      "Please input the white list of IP, separatedwith a space. [Default is: 0.0.0.0/0]: ") or "0.0.0.0/0"
    whitelist = models_util.check_network_whitelist(whitelist)
    netDict["whitelist"] = whitelist
    networkList.append(netDict)
  return networkList

def get_cluster_spec():
  task_types_str = compatibility_input("Please input distributed task type, separated with a space. [Default is: ps worker]: ") or 'ps worker'
  task_types = task_types_str.split(' ')

  cluster_spec = {}
  for task_type in task_types:
    count = compatibility_input("\nPlease input the count of '{}'. [Default is 1]: ".format(task_type)) or "1"
    count = models_util.check_distributed_count(count)
    cpu_limit = compatibility_input("Please input the cpu limit of '{}'. [Default is 1]: ".format(task_type)) or '1'
    cpu_limit = models_util.check_cpu_value(cpu_limit)
    memory_limit = compatibility_input("Please input the memory limit of '{}'. [Default is 1G]: ".format(task_type)) or '1G'
    memory_limit = models_util.check_memory_value(memory_limit)
    gpu_limit = compatibility_input("Please input the gpu limit of '{}'. [Defalut is 0]: ".format(task_type)) or "0"
    gpu_limit = models_util.check_gpu_value(gpu_limit)
    if gpu_limit > 0:
      gpu_type = compatibility_input("Please input the gpu type of '{}'. [Default is None]: ".format(task_type)) or None
      if isinstance(gpu_type, str) and gpu_type.lower() in constant.GPULIST:
        gpu_type = gpu_type.lower()
      elif gpu_type is not None:
        raise ValueError("Only three types of GPUs ({})".format("/".join(constant.GPULIST)))
    else:
      gpu_type = None
    task_args = compatibility_input("Please input the specific args of '{}'. [Default is '']: ".format(task_type)) or ""
    cluster_spec[task_type] = {
      'count': count,
      'cpu_limit': cpu_limit,
      'memory_limit': memory_limit,
      'gpu_limit': gpu_limit,
      'gpu_type': gpu_type,
      'task_args': task_args,
    }
  print("--------------------------\n")

  return cluster_spec

#For hptuning
def submit_hptuning(args):
  """Submit the hptuning"""
  # set environment variable to check args.trainer_uri

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  if args.filename:
    with open(args.filename) as f:
      try:
        hp_obj = json.load(f)
      except Exception as e:
        exit_as_error("ERROR: hptuning description json file({}) is not valid: {}".format(args.filename, e))
        return
      if not (("hp_name" in hp_obj) and ("module_name" in hp_obj) and
              ("trainer_uri" in hp_obj)):
        exit_as_error("ERROR: parameters hp_name, module_name and trainer_uri are necessary.")
        return
      # get the real and valid trainer_uri
      hp_obj["trainer_uri"] = models_util.validate_and_get_trainer_uri(str(hp_obj["trainer_uri"]))
      json_data = json.dumps(hp_obj)
  else:
    #TODO
    json_data=None
  response = client.submit_hptuning(json_data)
  if not isinstance(response, str):
    print_hp_job_info(response)
  else:
    print("response: {}".format(response))

def describe_hp_job(args):
  """Describe the hp job."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.describe_hp_job(args.hp_name, args.org_id)
  else:
    response = client.describe_hp_job(args.hp_name)
  if not isinstance(response, str):
    print_hp_job_info(response)
  else:
    print("response: {}".format(response))

def delete_hp(args):
  """Delete the job(s)."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    for hp_name in args.hp_names:
      response = client.delete_train_job(hp_name, args.org_id)
      print(response)
  else:
    for hp_name in args.hp_names:
      response = client.delete_hp_job(hp_name)
      print(response)

def list_hp(args):
    """List train jobs."""
    try:
      client = CloudMlClient()
    except Exception as e:
      exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
      return
    if "org_id" in args:
      if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
        response_hp_jobs = client.list_hp_jobs(
          constant.CLOUDML_ALL_ORG_PARAMETER)
      else:
        response_hp_jobs = client.list_hp_jobs(args.org_id)
    else:
      response_hp_jobs = client.list_hp_jobs()
    if not isinstance(response_hp_jobs, str):
      print_hp_list(response_hp_jobs, args)
    else:
      print("response: {}".format(response_hp_jobs))

def print_hp_list(response_hp_jobs, args):
    if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      print("{:16} {:16} {:32} {:16} {:32} {:32}".format(
        "ORG ID", "ORG NAME", "HP_NAME", "STATE", "CREATED", "UPDATED"))
      for hp_job in response_hp_jobs:
        print("{:<16} {:16} {:32} {:16} {:32} {:32}".format(hp_job[
                                                              "org_id"], hp_job["org_name"], hp_job["hp_name"],
                                                            color_util.colorize_state(hp_job["state"]),
                                                            hp_job["create_time"], hp_job["update_time"]))
    else:
      print("{:32} {:16} {:32} {:32}".format("JOB_NAME", "STATE", "CREATED",
                                             "UPDATED"))
      for hp_job in response_hp_jobs:
        print("{:32} {:16} {:32} {:32}".format(hp_job[
                                                 "hp_name"], color_util.colorize_state(hp_job["state"]),
                                               hp_job["create_time"], hp_job["update_time"]))

def get_trials(args):
  """list the trials of certain hp job"""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if not args.hp_name:
    exit_as_error ("ERROR: parameter hp_name cannot be None.")
    return
  response=client.list_hp_trials(args.hp_name)
  if not isinstance(response,str):
    print("response: {}".format(yaml.safe_dump(response,default_flow_style=False)))
  else:
    print(response)

def get_trial_log(args):
  """log of the trial"""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  extra_args = dict()
  if "follow" in args:
    extra_args = {"follow": args.follow}
  if "lines" in args and args.lines:
    extra_args["lines"] = args.lines
  if "org_id" in args:
    extra_args["org_id"] = args.org_id

  if not (args.hp_name and args.trial_id):
    exit_as_error("ERROR: parameters hp_name and trial_id cannot be None.")
    return
  response = client.get_hp_trial_logs(args.hp_name,args.trial_id, **extra_args)

  if "follow" in args and args.follow:
    try:
      for line in response.iter_lines():
        print(line)
    except KeyboardInterrupt:
      # exit silently
      return
    except requests.exceptions.ChunkedEncodingError as e:
      if "IncompleteRead(0 bytes read)" in str(e):
        # exit duo to no data read, maybe timeout
        exit_as_error("INFO: 0 bytes read, maybe closed by server due to timeout(5 mins).")
        return
      else:
        exit_as_error("ERROR: read log got ChunkedEncodingError: {}".format(e))
        return
    except Exception as e:
      exit_as_error("ERROR: read log got Error: {}".format(e))
      return
  else:
    # NOTE(xychu): compatible with old version client needed response format.
    # this format will be removed from the server side after no user using
    # client older than 0.2.21
    if not isinstance(response, str):
      response = response.json()
      if "error" in response and response["error"]:
        print(response)
      else:
        print(response["logs"])

def get_hp_job_events(args):
  """Get events of the hp job."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.get_hp_job_events(args.hp_name, args.org_id)
  else:
    response = client.get_hp_job_events(args.hp_name)
  if not isinstance(response, str):
    print_kubernetes_events(response["events"])
  else:
    print("response: {}".format(response))

def get_hp_metrics(args):
  """Get the metrics of the hp job."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.get_hp_job_metrics(args.hp_name, args.org_id)
  else:
    response = client.get_hp_job_metrics(args.hp_name)
  if not isinstance(response, str):
    print_metrics_result(response)
  else:
    print("response: {}".format(response))

def submit_job(args):
  """Submit the job."""
  # set environment variable to check args.trainer_uri
  if args.fds_endpoint:
    os.environ["XIAOMI_FDS_ENDPOINT"] = args.fds_endpoint
  if args.fds_bucket:
    os.environ["CLOUDML_DEFAULT_FDS_BUCKET"] = args.fds_bucket

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  args_dict = vars(args)
  if args.filename:
    with open(args.filename) as f:
      # TODO: Check file format and verify the items
      try:
        json_data = yaml.safe_load(f)
      except Exception as e:
        exit_as_error("ERROR: job description json file({}) is not valid: {}".format(args.filename, e))
        return
      for key in json_data:
        if key in args_dict and not args_dict[key]:
          args_dict[key] = json_data[key]

  if not (args.job_name and args.module_name and args.trainer_uri):
    exit_as_error(
        "ERROR: parameters job_name, module_name and trainer_uri cannot be None.")
    return

  try:
    train_job = TrainJob(args.job_name, args.module_name, args.trainer_uri)

    if (args.cpu_limit or args.memory_limit or args.gpu_limit or args.gpu_type) and args.distributed:
      print("When use -D(--distributed) para, don't set resource limit by -c(--cpu_limit), -M(--memory_limit) or -g(--gpu_limit) and -gt(--gpu_type)")
      print("The resource limit of distributed jobs should be provied followed.")
      exit_as_error("Exited!")
      return

    if args.cluster_spec:
      if isinstance(args.cluster_spec, str):
        try:
          train_job._cluster_spec = json.loads(args.cluster_spec)
        except Exception as e:

          exit_as_error("The cluster spec format should be json")
          return
      else:
        train_job._cluster_spec = args.cluster_spec
    elif args.distributed:
      train_job._cluster_spec = get_cluster_spec()
    if args.ps_count:
      train_job.ps_count = int(args.ps_count)
    if args.worker_count:
      train_job.worker_count = int(args.worker_count)
    if args.fds_endpoint:
      train_job.fds_endpoint = args.fds_endpoint
    elif client.fds_endpoint:
      train_job.fds_endpoint = client.fds_endpoint
    if args.fds_bucket:
      train_job.fds_bucket = args.fds_bucket
    elif client.fds_bucket:
      train_job.fds_bucket = client.fds_bucket
    # for hdfs
    if args.hdfs_krb_account:
      train_job.hdfs_krb_account = args.hdfs_krb_account
    elif client.hdfs_krb_account:
      train_job.hdfs_krb_account = client.hdfs_krb_account
    if args.hdfs_krb_password:
      train_job.hdfs_krb_password = args.hdfs_krb_password
    elif client.hdfs_krb_password:
      train_job.hdfs_krb_password = client.hdfs_krb_password
    if args.hdfs_endpoint:
      if args.hdfs_endpoint.startswith("hdfs://"):
        train_job.hdfs_endpoint = args.hdfs_endpoint
      else:
        raise ValueError("ERROR: -he[hdfs_endpoint] must start with hdfs://")
    elif client.hdfs_endpoint:
      train_job.hdfs_endpoint = client.hdfs_endpoint
    if args.hdfs_krb_keytab:
      train_job.hdfs_krb_keytab = args.hdfs_krb_keytab
    if train_job.hdfs_krb_account:
      if not train_job.hdfs_krb_password and not train_job.hdfs_krb_keytab:
        raise ValueError("ERROR: either -hkp[hdfs_krb_password] or -hkt[hdfs_krb_keytab] is required")
      if not train_job.hdfs_endpoint:
        raise ValueError("ERROR: -he[hdfs_endpoint] is required")
    elif train_job.hdfs_endpoint:
      raise ValueError("ERROR: -hka[hdfs_krb_account] is required")
    if args.job_args:
      train_job.job_args = args.job_args
    if args.cpu_limit:
      train_job.cpu_limit = args.cpu_limit
    if args.memory_limit:
      train_job.memory_limit = args.memory_limit
    if args.gpu_limit:
      train_job.gpu_limit = args.gpu_limit
    if args.framework:
      train_job.framework = args.framework
    if args.framework_version:
      train_job.framework_version = args.framework_version
    if args.docker_image:
      train_job.docker_image = args.docker_image
    if args.docker_command:
      train_job.docker_command = args.docker_command
    if args.volume_type:
      train_job.volume_type = args.volume_type
    if args.volume_path:
      train_job.volume_path = args.volume_path
    if args.mount_path:
      train_job.mount_path = args.mount_path
    if args.mount_read_only:
      if args.mount_read_only == "true" or args.mount_read_only == "True":
        train_job.mount_read_only = True
      else:
        train_job.mount_read_only = False
    if args.prepare_command:
      train_job.prepare_command = args.prepare_command
    if args.finish_command:
      train_job.finish_command = args.finish_command
    if args.node_selector_key:
      train_job.node_selector_key = args.node_selector_key
    if args.node_selector_value:
      train_job.node_selector_value = args.node_selector_value
    if args.gpu_type:
      if args.gpu_limit:
        train_job.gpu_type = args.gpu_type
      else:
        raise ValueError("ERROR: If you want select gpu type, gpu limit (-g) cannot be None.")
    if args.enable_rank:
      train_job.enable_rank = 1
    else:
      train_job.enable_rank = 0

    if args.save_mode:
      train_job.save_mode = args.save_mode

    if args.argo_mode:
      train_job.argo_mode = args.argo_mode

    if args.tensorboard_logdir:
      train_job.tensorboard_logdir = args.tensorboard_logdir

    if args.model_name:
      train_job.model_name = args.model_name
    if args.model_version:
      train_job.model_version = args.model_version
  except ValueError as e:
    exit_as_error("Error init TrainJob({}): {}".format(args.job_name, e))
    return

  json_data = train_job.get_json_data()

  if args.watch:
    job_name = args.job_name

  response = client.submit_train_job(json_data)
  if args.argo_mode:
    while True:
      response_state = client.describe_train_job(args.job_name)
      response_state = response_state["state"]
      if response_state in [constant.JOB_STATE_COMPLETED, constant.JOB_STATE_MODELSERVED]:
        break
      elif response_state == constant.JOB_STATE_FAILED:
        exit_as_error("Train job failed.")
      time.sleep(constant.ARGO_COMMAND_WAIT)
    response = client.get_train_job_logs(args.job_name)
  if not isinstance(response, str):
    if args.argo_mode:
      response = response.json()
      if "error" in response and response["error"]:
        exit_as_error(response)
      else:
        print(response["logs"])
    else:
      print_train_job_info(response)
    if args.watch:
      print("\nThe job has submitted, feel free to Ctrl+C to stop watching\n")
      print("{:32} {:16} {:32} {:32}".format("JOB_NAME", "STATE", "CREATED",
                                             "UPDATED"))
      while True:
        watch_response = client.describe_train_job(job_name)
        if not isinstance(watch_response, str):
          print("{:32} {:16} {:32} {:32}".format(watch_response[
                "job_name"], color_util.colorize_state(watch_response["state"]),
                watch_response["create_time"], watch_response["update_time"]))
          if watch_response["state"] == constant.JOB_STATE_COMPLETED:
            return
          try:
            time.sleep(constant.JOB_WATCH_INTERVAL)
          except KeyboardInterrupt:
            return
        else:
          return
  else:
    print("response: {}".format(response))


def describe_job(args):
  """Describe the job."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.describe_train_job(args.job_name, args.org_id)
  else:
    response = client.describe_train_job(args.job_name)
  if not isinstance(response, str):
    print_train_job_info(response)
  else:
    print("response: {}".format(response))


def get_job_logs(args):
  """Get the logs of the job."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  extra_args = dict()
  if "follow" in args:
    extra_args = {"follow": args.follow}
  if "lines" in args and args.lines:
    extra_args["lines"] = args.lines
  if "org_id" in args:
    extra_args["org_id"] = args.org_id

  response = client.get_train_job_logs(args.job_name, **extra_args)

  if "follow" in args and args.follow:
    try:
      for line in response.iter_lines():
        print(line)
    except KeyboardInterrupt:
      # exit silently
      return
    except requests.exceptions.ChunkedEncodingError as e:
      if "IncompleteRead(0 bytes read)" in str(e):
        # exit duo to no data read, maybe timeout
        exit_as_error("INFO: 0 bytes read, maybe closed by server due to timeout(5 mins).")
        return
      else:
        exit_as_error("ERROR: read log got ChunkedEncodingError: {}".format(e))
        return
    except Exception as e:
      exit_as_error("ERROR: read log got Error: {}".format(e))
      return
  else:
    # NOTE(xychu): compatible with old version client needed response format.
    # this format will be removed from the server side after no user using
    # client older than 0.2.21
    if not isinstance(response, str):
      response = response.json()
      if "error" in response and response["error"]:
        print(response)
      else:
        print(response["logs"])

def get_job_metrics(args):
  """Get the metrics of the job."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.get_train_job_metrics(args.job_name, args.org_id)
  else:
    response = client.get_train_job_metrics(args.job_name)
  if not isinstance(response, str):
    print_metrics_result(response)
  else:
    print("response: {}".format(response))


def get_job_hyperparameters_data(args):
  """Get hyperparameters data of the job."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  response = client.get_train_job_hyperparameters_data(args.job_name)
  if not isinstance(response, str):
    print_hyperparameter_data_result(response)
  else:
    print("response: {}".format(response))


def delete_job(args):
  """Delete the job(s)."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  extra_args = dict()
  if "is_cluster_name" in args:
    extra_args = {"is_cluster_name": args.is_cluster_name}
  if "org_id" in args:
    for job_name in args.job_names:
      response = client.delete_train_job(job_name, args.org_id, **extra_args)
      print(response)
  else:
    for job_name in args.job_names:
      response = client.delete_train_job(job_name, **extra_args)
      print(response)


def get_train_job_events(args):
  """Get events of the train job."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.get_train_job_events(args.job_name, args.org_id)
  else:
    response = client.get_train_job_events(args.job_name)
  if not isinstance(response, str):
    print_kubernetes_events(response["events"])
    if response["recommend"]:
      print_recommend_resource(response["recommend"])
  else:
    print("response: {}".format(response))


def start_job(args):
  """Start the job."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  response = client.start_train_job(args.job_name)
  if not isinstance(response, str):
    print_train_job_info(response)
  else:
    print("response: {}".format(response))


def list_models(args):
  """List model services."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      response_models = client.list_model_services(
          constant.CLOUDML_ALL_ORG_PARAMETER)
    else:
      response_models = client.list_model_services(args.org_id)
  else:
    response_models = client.list_model_services()
  if not isinstance(response_models, str):
    print_model_list(response_models, args)
  else:
    print("response: {}".format(response_models))

def print_model_list(response_models, args):
  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    print("{:16} {:16} {:32} {:16} {:32} {:16} {:32} {:32}".format(
      "ORG ID", "ORG NAME", "MODEL_NAME", "MODEL_VERSION", "ADDRESS",
      "STATE", "CREATED", "UPDATED"))
    for model in response_models:
      print("{:16} {:16} {:32} {:16} {:32} {:16} {:32} {:32}".format(model[
                                                                       "org_id"], model["org_name"],
                                                                     model["model_name"], model[
                                                                       "model_version"], model["address"],
                                                                     color_util.colorize_state(model["state"]), model[
                                                                       "create_time"], model["update_time"]))
  else:
    print("{:32} {:16} {:32} {:16} {:32} {:32}".format(
      "MODEL_NAME", "MODEL_VERSION", "ADDRESS", "STATE", "CREATED",
      "UPDATED"))
    for model in response_models:
      print("{:32} {:16} {:32} {:16} {:32} {:32}".format(model[
                                                           "model_name"], model["model_version"], model["address"],
                                                         color_util.colorize_state(model["state"]),
                                                         model["create_time"], model["update_time"]))

def create_model(args):
  """Create the model service."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  model = ModelService(args.model_name, args.model_version, args.model_uri)

  if args.fds_endpoint:
    model.fds_endpoint = args.fds_endpoint
  elif client.fds_endpoint:
    model.fds_endpoint = client.fds_endpoint
  if args.fds_bucket:
    model.fds_bucket = args.fds_bucket
  elif client.fds_bucket:
    model.fds_bucket = client.fds_bucket
  if args.model_args:
    model.model_args = args.model_args
  if args.cpu_limit:
    model.cpu_limit = args.cpu_limit
  if args.memory_limit:
    model.memory_limit = args.memory_limit
  if args.gpu_limit:
    model.gpu_limit = args.gpu_limit
  if args.framework:
    model.framework = args.framework
  if args.framework_version:
    model.framework_version = args.framework_version
  if args.docker_image:
    model.docker_image = args.docker_image
  if args.docker_command:
    model.docker_command = args.docker_command
  if args.replicas:
    model.replicas = int(args.replicas)
  if args.prepare_command:
    model.prepare_command = args.prepare_command
  if args.finish_command:
    model.finish_command = args.finish_command
  if args.node_selector_key:
    model.node_selector_key = args.node_selector_key
  if args.node_selector_value:
    model.node_selector_value = args.node_selector_value
  if args.gpu_type:
    if args.gpu_limit:
      model.gpu_type = args.gpu_type
    else:
      raise ValueError("ERROR: If you want select gpu type, gpu limit (-g) cannot be None.")
  if args.enable_rank:
    model.enable_rank = 1
  else:
    model.enable_rank = 0
  if args.debug:
    model.debug = 1
  else:
    model.debug = 0
  if args.watch:
    model_name = args.model_name
    model_version = args.model_version
  if args.save_mode:
    model.save_mode = args.save_mode
  if args.use_seldon:
    model.use_seldon = args.use_seldon
  if args.engine_cpu:
    model.engine_cpu = args.engine_cpu
  if args.engine_mem:
    model.engine_mem = args.engine_mem
  if args.run_class_name:
    model.run_class_name = args.run_class_name
  if args.service_schema:
    model.service_schema = args.service_schema
  if args.initial_delay_sec:
    model.initial_delay_sec = args.initial_delay_sec
  if args.pod_replicas:
    model.pod_replicas = args.pod_replicas
  if args.use_http:
    model.use_http = args.use_http
  response = client.create_model_service(model)
  if not isinstance(response, str):
    print_model_service_info(response)
    if args.watch:
      print("\nThe model is creating, feel free to Ctrl+C to stop watching\n")
      print("{:32} {:4} {:16} {:32} {:32}".format(
              "Model_NAME",
              "VERSION",
              "STATE",
              "CREATED",
              "UPDATED"))
      while True:
        watch_response = client.describe_model_service(model_name, model_version)
        if not isinstance(watch_response, str):
          print("{:32} {:4} {:16} {:32} {:32}".format(
                watch_response["model_name"],
                watch_response["model_version"],
                color_util.colorize_state(watch_response["state"]),
                watch_response["create_time"],
                watch_response["update_time"]))
          if watch_response["state"] == constant.MODEL_STATE_RUNNING:
            return
          try:
            time.sleep(constant.JOB_WATCH_INTERVAL)
          except KeyboardInterrupt:
            return
        else:
          return
  else:
    print("response: {}".format(response))


def describe_model(args):
  """Describe the model service."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.describe_model_service(args.model_name,
                                             args.model_version, args.org_id)
  else:
    response = client.describe_model_service(args.model_name,
                                             args.model_version)
  if not isinstance(response, str):
    print_model_service_info(response)
  else:
    print("response: {}".format(response))

def start_model(args):
  """Start the model service."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  response = client.start_model_service(args.model_name, args.model_version)
  if not isinstance(response, str):
    print_model_service_info(response)
  else:
    print("response: {}".format(response))

def update_model(args):
  """Update the model service."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  update_json = {}
  if args.model_uri:
    update_json["model_uri"] = args.model_uri
  if args.replicas:
    update_json["replicas"] = int(args.replicas)
  if args.cpu_limit:
    update_json["cpu_limit"] = args.cpu_limit
  if args.memory_limit:
    update_json["memory_limit"] = args.memory_limit
  if args.gpu_limit:
    update_json["gpu_limit"] = args.gpu_limit
  if args.framework:
    update_json["framework"] = args.framework
  if args.engine_cpu:
    update_json["engine_cpu"] = args.engine_cpu
  if args.engine_mem:
    update_json["engine_mem"] = args.engine_mem
  if args.port and args.port.isdigit():
    update_json["port"] = args.port

  if "org_id" in args:
    response = client.update_model_service(args.model_name,
                                           args.model_version,
                                           update_json,
                                           args.org_id)
  else:
    response = client.update_model_service(args.model_name,
                                           args.model_version,
                                           update_json)
  if not isinstance(response, str):
    print_model_service_info(response)
  else:
    print("response: {}".format(response))

def get_model_logs(args):
  """Get logs of the model service."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    if "replica_index" in args and args.replica_index:
      response = client.get_model_service_logs(model_name = args.model_name,
                                               model_version = args.model_version,
                                               org_id = args.org_id,
                                               replica_index = args.replica_index)
    elif "proxy_logs" in args and args.proxy_logs:
      response = client.get_model_service_logs(model_name = args.model_name,
                                               model_version = args.model_version,
                                               org_id = args.org_id,
                                               proxy_logs = args.proxy_logs)
    else:
      response = client.get_model_service_logs(args.model_name, args.model_version, args.org_id)
  else:
    if "replica_index" in args and args.replica_index:
      response = client.get_model_service_logs(args.model_name, args.model_version, replica_index=args.replica_index)
    elif "proxy_logs" in args and args.proxy_logs:
      response = client.get_model_service_logs(model_name=args.model_name,
                                               model_version=args.model_version,
                                               proxy_logs=args.proxy_logs)
    else:
      response = client.get_model_service_logs(args.model_name, args.model_version)
  if not isinstance(response, str):
    if "error" in response:
      print(response['message'])
    else:
      print(response["logs"])
  else:
    print("response: {}".format(response))


def get_model_metrics(args):
  """Get the metrics of the model service."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.get_model_service_metrics(args.model_name, args.model_version, args.org_id)
  else:
    response = client.get_model_service_metrics(args.model_name, args.model_version)
  if not isinstance(response, str):
    print_metrics_result(response)
  else:
    print("response: {}".format(response))


def delete_model(args):
  """Delete the model service."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.delete_model_service(args.model_name, args.model_version, args.org_id)
  else:
    response = client.delete_model_service(args.model_name, args.model_version)
  print(response)


def get_model_service_events(args):
  """Get events of the model service."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.get_model_service_events(args.model_name,
                                               args.model_version, args.org_id)
  else:
    response = client.get_model_service_events(args.model_name,
                                               args.model_version)
  if not isinstance(response, str):
    print_kubernetes_events(response["events"])
    if response["recommend"]:
      print_recommend_resource(response["recommend"])
  else:
    print("response: {}".format(response))


def list_tensorboard_services(args):
  """List tensorboard_services."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      response_tensorboard = client.list_tensorboard_services(
          constant.CLOUDML_ALL_ORG_PARAMETER)
    else:
      response_tensorboard = client.list_tensorboard_services(args.org_id)
  else:
    response_tensorboard = client.list_tensorboard_services()

  if not isinstance(response_tensorboard, str):
    print_tensorboard_list(response_tensorboard, args)
  else:
    print("response: {}".format(response_tensorboard))

def print_tensorboard_list(response_tensorboard, args):
  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    print("{:16} {:16} {:32} {:60} {:10} {:32} {:32}".format(
      "ORG ID", "ORG NAME", "TENSORBOARD_NAME", "ADDRESS", "STATE",
      "CREATED", "UPDATED"))
    for tensorboard in response_tensorboard:
      print("{:16} {:16} {:32} {:60} {:10} {:32} {:32}".format(tensorboard[
                                                                 "org_id"], tensorboard["org_name"], tensorboard[
                                                                 "tensorboard_name"], tensorboard["address"],
                                                               color_util.colorize_state(tensorboard[
                                                                                           "state"]),
                                                               tensorboard["create_time"], tensorboard[
                                                                 "update_time"]))
  else:
    print("{:32} {:60} {:10} {:32} {:32}".format(
      "TENSORBOARD_NAME", "ADDRESS", "STATE", "CREATED", "UPDATED"))
    for tensorboard in response_tensorboard:
      print("{:32} {:60} {:10} {:32} {:32}".format(tensorboard[
                                                     "tensorboard_name"], tensorboard["address"],
                                                   color_util.colorize_state(tensorboard["state"]),
                                                   tensorboard["create_time"], tensorboard["update_time"]))


def create_tensorboard_service(args):
  """Create the tensorboard_service."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  tensorboard = TensorboardService(args.tensorboard_name, args.logdir)

  if args.framework:
    tensorboard.framework = args.framework
  if args.framework_version:
    tensorboard.framework_version = args.framework_version
  if args.docker_image:
    tensorboard.docker_image = args.docker_image
  if args.docker_command:
    tensorboard.docker_command = args.docker_command
  if args.fds_endpoint:
    tensorboard.fds_endpoint = args.fds_endpoint
  elif client.fds_endpoint:
    tensorboard.fds_endpoint = client.fds_endpoint
  if args.fds_bucket:
    tensorboard.fds_bucket = args.fds_bucket
  elif client.fds_bucket:
    tensorboard.fds_bucket = client.fds_bucket
  if args.node_selector_key:
    tensorboard.node_selector_key = args.node_selector_key
  if args.node_selector_value:
    tensorboard.node_selector_value = args.node_selector_value
  if args.enable_rank:
    tensorboard.enable_rank = 1
  else:
    tensorboard.enable_rank = 0

  response = client.create_tensorboard_service(tensorboard)
  if not isinstance(response, str):
    print_tensorboard_info(response)
  else:
    print("response: {}".format(response))


def describe_tensorboard_service(args):
  """Describe the tensorboard_service."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.describe_tensorboard_service(args.tensorboard_name,
                                                   args.org_id)
  else:
    response = client.describe_tensorboard_service(args.tensorboard_name)
  if not isinstance(response, str):
    print_tensorboard_info(response)
  else:
    print("response: {}".format(response))


def delete_tensorboard_service(args):
  """Delete the tensorboard_service(s)."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    for tensorboard_name in args.tensorboard_names:
      response = client.delete_tensorboard_service(tensorboard_name, args.org_id)
      print(response)
  else:
    for tensorboard_name in args.tensorboard_names:
      response = client.delete_tensorboard_service(tensorboard_name)
      print(response)


def get_tensorboard_service_events(args):
  """Get events of the tensorboard service."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  response = client.get_tensorboard_service_events(args.tensorboard_name)
  if not isinstance(response, str):
    print_kubernetes_events(response["events"])
    if response["recommend"]:
      print_recommend_resource(response["recommend"])
  else:
    print("response: {}".format(response))


def list_dev_envs(args):
  """List dev environments."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      response_dev_envs = client.list_dev_envs(
          constant.CLOUDML_ALL_ORG_PARAMETER)
    else:
      response_dev_envs = client.list_dev_envs(args.org_id)
  else:
    response_dev_envs = client.list_dev_envs()
  if not isinstance(response_dev_envs, str):
    if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      print("{:16} {:16} {:32} {:16} {:32} {:32}".format(
          "ORG ID", "ORG NAME", "DEV_NAME", "STATE", "CREATED",
          "UPDATED"))
      for dev_env in response_dev_envs:
        print("{:16} {:16} {:32} {:16} {:32} {:32}".format(dev_env[
            "org_id"], dev_env["org_name"], dev_env["dev_name"],
            color_util.colorize_state(dev_env["state"]), dev_env[
              "create_time"], dev_env["update_time"]))
    else:
      print("{:32} {:16} {:32} {:32}".format(
          "DEV_NAME", "STATE", "CREATED", "UPDATED"))
      for dev_env in response_dev_envs:
        print("{:32} {:16} {:32} {:32}".format(dev_env[
            "dev_name"], color_util.colorize_state(dev_env[
              "state"]), dev_env["create_time"], dev_env["update_time"]))
  else:
    print("response: {}".format(response_dev_envs))


def create_dev_env(args):
  """Create dev env."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  dev_env = DevEnv(args.dev_name, args.password)

  if args.fds_endpoint:
    dev_env.fds_endpoint = args.fds_endpoint
  elif client.fds_endpoint:
    dev_env.fds_endpoint = client.fds_endpoint
  if args.fds_bucket:
    dev_env.fds_bucket = args.fds_bucket
  elif client.fds_bucket:
    dev_env.fds_bucket = client.fds_bucket
  # for hdfs
  if args.hdfs_krb_account:
    dev_env.hdfs_krb_account = args.hdfs_krb_account
  elif client.hdfs_krb_account:
    dev_env.hdfs_krb_account = client.hdfs_krb_account
  if args.hdfs_krb_password:
    dev_env.hdfs_krb_password = args.hdfs_krb_password
  elif client.hdfs_krb_password:
    dev_env.hdfs_krb_password = client.hdfs_krb_password
  if args.hdfs_endpoint:
    if args.hdfs_endpoint.startswith("hdfs://"):
      dev_env.hdfs_endpoint = args.hdfs_endpoint
    else:
      raise ValueError("ERROR: -he[hdfs_endpoint] must start with hdfs://")
  elif client.hdfs_endpoint:
    dev_env.hdfs_endpoint = client.hdfs_endpoint
  if args.hdfs_krb_keytab:
    dev_env.hdfs_krb_keytab = args.hdfs_krb_keytab
  if dev_env.hdfs_krb_account:
    if not dev_env.hdfs_krb_password and not dev_env.hdfs_krb_keytab:
      raise ValueError("ERROR: either -hkp[hdfs_krb_password] or -hkt[hdfs_krb_keytab] is required")
    if not dev_env.hdfs_endpoint:
      raise ValueError("ERROR: -he[hdfs_endpoint] is required")
  elif dev_env.hdfs_endpoint:
    raise ValueError("ERROR: -hka[hdfs_krb_account] is required")

  if args.ceph_volume:
    dev_env.ceph_volume = args.ceph_volume
    if not args.ceph_mode:
      raise ValueError("ERROR: -cm[ceph_mode] cannot be empty")
    if args.ceph_mode != "r" and args.ceph_mode != "rw":
      raise ValueError("ERROR: invalid value for -cm[ceph_mode]")
    dev_env.ceph_mode = args.ceph_mode
  
  if args.cpu_limit:
    dev_env.cpu_limit = args.cpu_limit
  if args.memory_limit:
    dev_env.memory_limit = args.memory_limit
  if args.gpu_limit:
    dev_env.gpu_limit = args.gpu_limit
  if args.framework:
    dev_env.framework = args.framework
  if args.framework_version:
    dev_env.framework_version = args.framework_version
  if args.docker_image:
    dev_env.docker_image = args.docker_image
  if args.docker_command:
    dev_env.docker_command = args.docker_command
  if args.node_selector_key:
    dev_env.node_selector_key = args.node_selector_key
  if args.node_selector_value:
    dev_env.node_selector_value = args.node_selector_value
  if args.gpu_type:
    if args.gpu_limit:
      dev_env.gpu_type = args.gpu_type
    else:
      raise ValueError("ERROR: If you want select gpu type, gpu limit (-g) cannot be None.")
  if args.watch:
    dev_name = args.dev_name
  if args.network:
    dev_env.network = setNetwork()
  if args.enable_rank:
    dev_env.enable_rank = 1
  else:
    dev_env.enable_rank = 0

  response_dev_env = client.create_dev_env(dev_env.get_json_data())
  if not isinstance(response_dev_env, str):
    print_dev_env_info(response_dev_env)
    if args.watch:
      print("\nThe dev_env is creating, feel free to Ctrl+C to stop watching\n")
      print("{:32} {:16} {:32} {:32}".format(
              "DEV_NAME",
              "STATE",
              "CREATED",
              "UPDATED"))
      while True:
        watch_response = client.describe_dev_env(dev_name)
        if not isinstance(watch_response, str):
          print("{:32} {:16} {:32} {:32}".format(
                watch_response["dev_name"],
                color_util.colorize_state(watch_response["state"]),
                watch_response["create_time"],
                watch_response["update_time"]))
          if watch_response["state"] == constant.DEV_ENV_STATE_RUNNING:
            return
          try:

            time.sleep(constant.JOB_WATCH_INTERVAL)
          except KeyboardInterrupt:
            return
        else:
          return
  else:
    print("response: {}".format(response_dev_env))


def describe_dev_env(args):
  """Describe the dev environment."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.describe_dev_env(args.dev_name, args.org_id)
  else:
    response = client.describe_dev_env(args.dev_name)
  if not isinstance(response, str):
    print_dev_env_info(response)
  else:
    print("response: {}".format(response))

def stop_dev_env(args):
  """Stop the dev environment(s)."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    for dev_name in args.dev_names:
      response = client.stop_dev_env(dev_name, args.org_id)
      print(response)
  else:
    for dev_name in args.dev_names:
      response = client.stop_dev_env(dev_name)
      print(response)

def save_dev_env(args):
  """Save the dev environment(s)."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    for dev_name in args.dev_names:
      response = client.save_dev_env(dev_name, args.org_id)
      print(response)
  else:
    for dev_name in args.dev_names:
      response = client.save_dev_env(dev_name)
      print(response)

def restart_dev_env(args):
  """Restart the dev environment(s)."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    for dev_name in args.dev_names:
      response = client.restart_dev_env(dev_name, args.org_id)
      print(response)
  else:
    for dev_name in args.dev_names:
      response = client.restart_dev_env(dev_name)
      print(response)

def delete_dev_env(args):
  """Delete the dev environment(s)."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    for dev_name in args.dev_names:
      response = client.delete_dev_env(dev_name, args.org_id)
      print(response)
  else:
    for dev_name in args.dev_names:
      response = client.delete_dev_env(dev_name)
      print(response)

def get_dev_env_events(args):
  """Get events of the dev environment."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  response = client.get_dev_env_events(args.dev_name)
  if not isinstance(response, str):
    print_kubernetes_events(response["events"])
    if response["recommend"]:
      print_recommend_resource(response["recommend"])
  else:
    print("response: {}".format(response))


def get_dev_env_metrics(args):
  """Get the metrics of the dev environment."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  response = client.get_dev_env_metrics(args.dev_name)
  if not isinstance(response, str):
    print_metrics_result(response)
  else:
    print("response: {}".format(response))


def list_dev_servers(args):
  """List dev servers."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      response_dev_servers = client.list_dev_servers(
          constant.CLOUDML_ALL_ORG_PARAMETER)
    else:
      response_dev_servers = client.list_dev_servers(args.org_id)
  else:
    response_dev_servers = client.list_dev_servers()
  if not isinstance(response_dev_servers, str):
    if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      print("{:16} {:16} {:32} {:32} {:16} {:32} {:32}".format(
          "ORG ID", "ORG NAME", "DEV_NAME", "ADDRESS", "STATE", "CREATED",
          "UPDATED"))
      for dev_server in response_dev_servers:
        print("{:16} {:16} {:32} {:32} {:16} {:32} {:32}".format(
            dev_server["org_id"], dev_server["org_name"], dev_server[
                "dev_name"], dev_server["address"],
            color_util.colorize_state(dev_server["state"]),
            dev_server["create_time"], dev_server["update_time"]))
    else:
      print("{:32} {:32} {:16} {:32} {:32}".format(
          "DEV_NAME", "ADDRESS", "STATE", "CREATED", "UPDATED"))
      for dev_server in response_dev_servers:
        print("{:32} {:32} {:16} {:32} {:32}".format(
            dev_server["dev_name"], dev_server["address"],
            color_util.colorize_state(dev_server["state"]),
            dev_server["create_time"], dev_server["update_time"]))
  else:
    print("response: {}".format(response_dev_servers))


def create_dev_server(args):
  """Create dev server."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  dev_server = DevServer(args.dev_name, args.password)

  if args.framework:
    dev_server.framework = args.framework
  if args.framework_version:
    dev_server.framework_version = args.framework_version
  if args.docker_image:
    dev_server.docker_image = args.docker_image
  if args.docker_command:
    dev_server.docker_command = args.docker_command
  if args.enable_rank:
    dev_server.enable_rank = 1
  else:
    dev_server.enable_rank = 0
  response_dev_server = client.create_dev_server(dev_server)
  if not isinstance(response_dev_server, str):
    print_dev_server_info(response_dev_server)
  else:
    print("response: {}".format(response_dev_server))


def describe_dev_server(args):
  """Describe the dev server."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.describe_dev_server(args.dev_name, args.org_id)
  else:
    response = client.describe_dev_server(args.dev_name)
  if not isinstance(response, str):
    print_dev_server_info(response)
  else:
    print("response: {}".format(response))


def delete_dev_server(args):
  """Delete the dev server(s)."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  for dev_name in args.dev_names:
    response = client.delete_dev_server(dev_name)
    print(response)


def get_dev_server_events(args):
  """Get events of the dev server."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  response = client.get_dev_server_events(args.dev_name)
  if not isinstance(response, str):
    print_kubernetes_events(response["events"])
  else:
    print("response: {}".format(response))


def list_quota(args):
  """List the quota."""
  try:
      client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
      response_quotas = client.get_quota(args.org_id)
  else:
    response_quotas = client.get_quota()

  if not isinstance(response_quotas, str):
    if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      for quota in response_quotas:
        print("\nThe quota of user {}-{}:".format(quota["org_id"], quota[
            "org_name"]))
        print_quota_info(quota)
    else:
      for quota in response_quotas:
        print_quota_info(quota)
  else:
    print(response_quotas)


def apply_quota(args):
  """Apply for a quota update."""

  if not (args.type == "dev"
        or args.type == "jobs"
        or args.type == "models"):
    print("ERROR: Unknown job type {}.".format(args.type))
  else:
    try:
      client = CloudMlClient()
    except Exception as e:
      exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
      return
    response_quotas = client.get_quota()
    if not len(response_quotas) == 1:
        print("ERROR: Failed to get org mail")
    else:
        quota = response_quotas[0]
        org_id=quota["org_id"]
        org_name=quota["org_name"]
        org_mail=quota["org_mail"]

        if not org_mail:
          print("ERROR: Please set org mail first via 'cloudml config init'")
        else:
          data = {
            "org_id": org_id,
            "org_name": org_name,
            "org_mail": org_mail,
          }
          data["region"]=client.endpoint
          data["service"]=args.type
          data["cpu_limit"]=args.cpu_limit
          data["memory_limit"]=args.memory_limit
          data["gpu_limit"]=args.cpu_limit

          response = client.apply_quota(data)

          if not isinstance(response, str) and ("{}".format(response["error"]).lower() == "false"):
            print("Your application has been submitted for approval")
          else:
            print("response: {}".format(response))


def do_predict(args):
  """Do predict."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  # TODO: Remove duplicated code
  if args.timeout:
    if args.model_version:
      response = client.do_predict(args.model_name, args.model_version,
                                   args.filename, float(args.timeout))
    elif args.server:
      response = client.do_predict_server(args.server, args.model_name,
                                          args.filename, float(args.timeout))
    else:
      exit_as_error("Need to set either model_version or server, exit now.")
      return 1
  else:
    if args.model_version:
      response = client.do_predict(args.model_name, args.model_version,
                                   args.filename)
    elif args.server:
      response = client.do_predict_server(args.server, args.model_name,
                                          args.filename)
    else:
      exit_as_error("Need to set either model_version or server, exit now.")
      return 1
  if isinstance(response, str):
    print(response)
  else:
    print_predict_result(response)


def update_job_quota(args, quota):
  if args.cpu:
    quota.train_cpu_quota = args.cpu
  if args.memory:
    quota.train_memory_quota = args.memory
  if args.gpu:
    quota.train_gpu_quota = int(args.gpu)
  if args.count:
    quota.train_count_quota = int(args.count)
  if args.priority_quota:
    quota.train_priority_quota = args.priority_quota
  if args.priority:
    quota.train_priority_rank = args.priority
  return quota


def update_model_quota(args, quota):
  if args.cpu:
    quota.model_cpu_quota = args.cpu
  if args.memory:
    quota.model_memory_quota = args.memory
  if args.gpu:
    quota.model_gpu_quota = int(args.gpu)
  if args.count:
    quota.model_count_quota = int(args.count)
  if args.priority_quota:
    quota.model_priority_quota = args.priority_quota
  if args.priority:
    quota.model_priority_rank = args.priority
  return quota


def update_dev_quota(args, quota):
  if args.cpu:
    quota.dev_cpu_quota = args.cpu
  if args.memory:
    quota.dev_memory_quota = args.memory
  if args.gpu:
    quota.dev_gpu_quota = int(args.gpu)
  if args.count:
    quota.dev_count_quota = int(args.count)
  if args.priority_quota:
    quota.dev_priority_quota = args.priority_quota
  if args.priority:
    quota.dev_priority_rank = args.priority
  return quota


def update_tensorboard_quota(args, quota):
  if args.tensorboard:
    quota.tensorboard_quota = int(args.tensorboard)
  if args.priority_quota:
    quota.tensorboard_priority_quota = args.priority_quota
  if args.priority:
    quota.tensorboard_priority_rank = args.priority
  return quota


def update_total_quota(args, quota):
  if args.cpu:
    quota.total_cpu_quota = args.cpu
  if args.memory:
    quota.total_memory_quota = args.memory
  if args.gpu:
    quota.total_gpu_quota = int(args.gpu)
  return quota


def update_quota(args):
  if not (args.cpu or args.memory or args.gpu or args.tensorboard or
          args.count or args.priority_quota or args.priority or args.org_mail or args.project):
    print("ERROR: Please give the resource to change")
  else:
    quota = Quota(args.org_id, args.org_name)

    if args.type == "jobs":
      quota = update_job_quota(args, quota)
    elif args.type == "models":
      quota = update_model_quota(args, quota)
    elif args.type == "dev":
      quota = update_dev_quota(args, quota)
    elif args.type == "tensorboard":
      quota = update_tensorboard_quota(args, quota)
    elif args.type == "total":
      quota = update_total_quota(args, quota)

    # update the other fields, they can be update separately or along with type parameter
    if args.org_mail:
      quota.org_mail = args.org_mail

    if args.project:
      quota.project = args.project

    try:
      client = CloudMlClient()
    except Exception as e:
      exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
      return
    response_quota = client.update_quota(quota)
    if not isinstance(response_quota, str):
      print_quota_info(response_quota)
    else:
      print("response: {}".format(response_quota))

    print("updated")


def list_framework(args):
  """List the framework."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  response = client.get_frameworks()

  if not isinstance(response, str):
    print_frameworks_info(response)
  else:
    print("response: {}".format(response))


def list_pipelines(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    response = client.list_pipelines(constant.CLOUDML_ALL_ORG_PARAMETER)
  else:
    response = client.list_pipelines()
  if not isinstance(response, str):
    print_pipeline_list(response, args)
  else:
    print("response: {}".format(response))


def list_pipeline_schedules(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    response = client.list_pipeline_schedules(args.pipeline_name, constant.CLOUDML_ALL_ORG_PARAMETER)
  else:
    response = client.list_pipeline_schedules(args.pipeline_name)
  if not isinstance(response, str):
    print_pipeline_schedule_list(response, args)
  else:
    print("response: {}".format(response))


def create_pipeline_schedule(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  if not args.pipeline_rerun_date:
    schedule_param = {
      "pipeline_rerun_date": datetime.now().strftime("%Y%m%d")
    }
  else:
    schedule_param = {
      "pipeline_rerun_date": args.pipeline_rerun_date
    }
  request_data = {
    "schedule_param": schedule_param
  }
  response = client.create_pipeline_schedule(json.dumps(request_data), args.pipeline_name)
  print("response: {}".format(response))

def describe_pipeline_schedule(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    response = client.describe_pipeline_schedules(args.schedule_id, constant.CLOUDML_ALL_ORG_PARAMETER)
  else:
    response = client.describe_pipeline_schedule(args.schedule_id)

  if not isinstance(response, str):

    print_pipeline_schedule_info(response)
  else:
    print("response: {}".format(response))


def print_pipeline_list(response, args):
  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    print("{:16} {:16} {:32} {:32} {:32} {:32}".format(
      "ORG ID", "ORG NAME", "PIPELINE_NAME",
      "STATE", "CREATED", "UPDATED"))
    for pipeline in response:
      print("{:<16} {:16} {:32} {:16} {:32} {:32}".format(pipeline["org_id"], pipeline["org_name"],
                                                          pipeline["pipeline_name"], pipeline["state"],
                                                          pipeline["create_time"], pipeline["update_time"]))
  else:
    print("{:32} {:32} {:32} {:32}".format("PIPELINE_NAME",
                                                       "STATE", "CREATED",
                                                       "UPDATED"))

    for pipeline in response:
      print("{:32} {:32} {:32} {:32}".format(pipeline["pipeline_name"], pipeline["state"],
                                                         pipeline["create_time"], pipeline["update_time"]))

def print_pipeline_schedule_list(response, args):
  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    print("{:16} {:16} {:16} {:32} {:32} {:32} {:32}".format(
      "ORG ID", "ORG NAME","SCHEDULE_ID", "PIPELINE_NAME",
      "STATE", "CREATED", "UPDATED"))
    for pipeline in response:
      print("{:<16} {:16} {:16}  {:32} {:16} {:32} {:32}".format(pipeline["org_id"], pipeline["org_name"],pipeline["id"],
                                                          pipeline["pipeline_name"], pipeline["state"],
                                                          pipeline["create_time"], pipeline["update_time"]))
  else:
    print(" {:16} {:32} {:32} {:32} {:32}".format("SCHEDULE_ID", "PIPELINE_NAME",
                                                       "STATE", "CREATED",
                                                       "UPDATED"))

    for pipeline in response:
      print(" {:16} {:32} {:32} {:32} {:32}".format(pipeline["id"], pipeline["pipeline_name"], pipeline["state"],
                                                         pipeline["create_time"], pipeline["update_time"]))

def delete_pipeline(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  for pipeline_name in args.pipeline_names:
    response = client.delete_pipeline(pipeline_name)
    print(response)

def describe_pipeline(args):
  """Describe the pipeline."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.describe_pipeline(args.pipeline_name, args.org_id)
  else:
    response = client.describe_pipeline(args.pipeline_name)

  if not isinstance(response, str):
  #  print("{:32} {:32} {:32} {:32} {:32} {:32}".format(pipeline[
  #                                               "pipeline_name"],pipeline["waiting_nodes"],
  #                                             pipeline["processing_nodes"],pipeline['finished_nodes'],
  #                                             pipeline["create_time"], pipeline["update_time"]))
    print_pipeline_info(response)

  else:
    print("response: {}".format(response))


def get_pipeline_logs(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.get_pipeline_logs(args.pod_name, args.org_id)
  else:
    response = client.get_pipeline_logs(args.pod_name)
  if not isinstance(response, str):
    logs = response["data"]['argo_log_info']
    print("###########################################")
    print("LOGS OF POD {}".format(args.pod_name))
    print("###########################################")
    print(logs)

  else:
    print("response:{}".format(response))


def start_pipeline(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.start_pipeline(args.pipeline_name, args.org_id)
  else:
    response = client.start_pipeline(args.pipeline_name)
  print(response)

def stop_pipeline(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.stop_pipeline(args.pipeline_name, args.org_id)
  else:
    response = client.stop_pipeline(args.pipeline_name)
  print(response)

def rerun_pipeline(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    print("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  data = {}
  data['start_node'] = args.start_node
  data['date_range'] = args.date_range
  json_data = json.dumps(data)
  response = client.rerun_pipeline(args.pipeline_name, json_data)
  print(response) 

def create_pipeline(args):
  return create_or_update_pipeline(args, True)
def update_pipeline(args):
  return create_or_update_pipeline(args, False)
def create_or_update_pipeline(args, is_create=True):
  """Submit the job."""

  # set environment variable to check args
  if args.fds_endpoint:
    os.environ["XIAOMI_FDS_ENDPOINT"] = args.fds_endpoint
  if args.fds_bucket:
    os.environ["CLOUDML_DEFAULT_FDS_BUCKET"] = args.fds_bucket

  args_dict = vars(args)
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if args.filename:
    with open(args.filename) as f:
      # TODO: Check file format and verify the items
      json_data = yaml.safe_load(f)
      for key in json_data :
        if key in args_dict and not args_dict[key]:
          args_dict[key] = json_data[key]

  if not args.pipeline_name:
    exit_as_error("ERROR: parameters pipeline_name is necessary.")
    return

  pipeline = Pipeline(args.pipeline_name)

  if 'pipeline_config' not in args or args.pipeline_config is None:
    raise ValueError('ERROR: pipeline_config is necessary')

  if isinstance(args.pipeline_config, dict):
    # json file load to the args.pipeline_config
    args.pipeline_config = json.dumps(args.pipeline_config)
  pipeline.pipeline_config = args.pipeline_config


  if args.fds_endpoint:
    pipeline.fds_endpoint = args.fds_endpoint
  elif client.fds_endpoint:
    pipeline.fds_endpoint = client.fds_endpoint
  if args.fds_bucket:
    pipeline.fds_bucket = args.fds_bucket
  elif client.fds_bucket:
    pipeline.fds_bucket = client.fds_bucket
  # for hdfs
  if args.hdfs_krb_account:
    pipeline.hdfs_krb_account = args.hdfs_krb_account
  elif client.hdfs_krb_account:
    pipeline.hdfs_krb_account = client.hdfs_krb_account
  if args.hdfs_krb_password:
    pipeline.hdfs_krb_password = args.hdfs_krb_password
  elif client.hdfs_krb_password:
    pipeline.hdfs_krb_password = client.hdfs_krb_password
  if args.hdfs_endpoint:
    if args.hdfs_endpoint.startswith("hdfs://"):
      pipeline.hdfs_endpoint = args.hdfs_endpoint
    else:
      raise ValueError("ERROR: -he[hdfs_endpoint] must start with hdfs://")
  elif client.hdfs_endpoint:
    pipeline.hdfs_endpoint = client.hdfs_endpoint

  if args.hdfs_krb_keytab:
    pipeline.hdfs_krb_keytab = args.hdfs_krb_keytab

  if pipeline.hdfs_krb_account:
    if not pipeline.hdfs_krb_password and not pipeline.hdfs_krb_keytab:
      raise ValueError("ERROR: either -hkp[hdfs_krb_password] or -hkt[hdfs_krb_keytab] is required")
    if not pipeline.hdfs_endpoint:
      raise ValueError("ERROR: -he[hdfs_endpoint] is required")
  elif pipeline.hdfs_endpoint:
    raise ValueError("ERROR: -hka[hdfs_krb_account] is required")

  if args.cloudml_endpoint:
    if args.cloudml_endpoint.startswith("http"):
      pipeline.cloudml_endpoint = args.cloudml_endpoint
    else:
      raise ValueError("ERROR: -he[cloudml_endpoint] must start with http")
  else:
    pipeline.cloudml_endpoint = client.endpoint

  if args.save_mode:
    pipeline.save_mode = args.save_mode

  if args.org_mail:
    if '@' in args.org_mail:
      pipeline.org_mail = args.org_mail
    else:
      raise ValueError("ERROR: org_mail must contains '@'")
  else:
    pipeline.org_mail = args.org_mail

  json_data = pipeline.get_json_data()
  if is_create:
    response = client.create_pipeline(json_data)
  else:
    response = client.update_pipeline(json_data, args.pipeline_name)

  if not isinstance(response, str):
    print_pipeline_info(response)
    if args.watch:
      print("\nThe pipeline has created, feel free to Ctrl+C to stop watching\n")
      print("{:32} {:16} {:32} {:32}".format("PIPELINE_NAME", "STATE", "CREATED",
                                             "UPDATED"))
      while True:
        watch_response = client.describe_pipeline(pipeline.pipeline_name)
        if not isinstance(watch_response, str):
          print_pipeline_info(watch_response, args)
          if watch_response["state"] in (constant.PIPELINE_STATE_COMPLETED, constant.PIPELINE_STATE_FAILED):
            return
          try:
            time.sleep(constant.PIPELINE_WATCH_INTERVAL)
          except KeyboardInterrupt:
            return
        else:
          return
  else:
    print("response: {}".format(response))

def print_schedule_list(response, args):
  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    print("{:16} {:16} {:32} {:32} {:16} {:16} {:16} {:32}".format(
      "ORG ID", "ORG NAME", "SCHEDULE_NAME", "RESOURCE_NAME",
                        "RESOURCE_TYPE", "CRON_PARAM", "SUSPEND", "LAST_CREATE_TIME"))
    for schedule in response:
      suspend = "True" if schedule["suspend"] else "False"
      print("{:<16} {:16} {:32} {:32} {:16} {:16} {:16} {:32}".format(schedule["org_id"], schedule["org_name"],
                                                          schedule["schedule_name"], schedule["resource_name"],
                                                          schedule["resource_type"], schedule["cron_param"],
                                                                      suspend, schedule["last_create_time"]))
  else:
    print("{:32} {:32} {:16} {:16} {:16} {:32}".format("SCHEDULE_NAME",
                                                       "RESOURCE_NAME", "RESOURCE_TYPE", "CRON_PARAM","SUSPEND",  "LAST_CREATE_TIME"))
    for schedule in response:
      suspend = "True" if schedule["is_suspend"] else "False"
      print("{:32} {:32} {:16} {:16} {:16} {:32}".format(schedule["schedule_name"], schedule["resource_name"],
                                                         schedule["resource_type"], schedule["cron_param"],
                                                         suspend, schedule["last_create_time"]))
def print_schedule_info(response):
  """Print train job in customed format.

  Args:
    schedule: The dictionary of response train job data.
  """

  schedule = response['data']
  print("{:16} {}".format("Org id:", schedule["org_id"]))
  print("{:16} {}".format("Org name:", schedule["org_name"]))
  print("{:16} {}".format("schedule name:", schedule["schedule_name"]))
  print("{:16} {}".format("resource_name:", schedule["resource_name"]))
  print("{:16} {}".format("resource_type:", schedule["resource_type"]))
  print("{:16} {}".format("cron_param:", schedule["cron_param"]))
  print("{:16} {}".format("concurrency_policy:", schedule["concurrency_policy"]))
  print("{:16} {}".format("image_name:", schedule["image_name"]))
  print("{:16} {}".format("is_active:", schedule["is_active"]))
  print("{:16} {}".format("last_schedule:", schedule["last_schedule"]))
  print("{:16} {}".format("last_create_time:", schedule["last_create_time"]))
  print("{:16} {}".format("is_suspend:", schedule["is_suspend"]))


def list_schedules(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    response = client.list_schedules(constant.CLOUDML_ALL_ORG_PARAMETER)
  else:
    response = client.list_schedules()
  if not isinstance(response, str):
    print_schedule_list(response, args)
  else:
    print("response: {}".format(response))


def delete_schedule(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  for schedule_name in args.schedule_names:
    response = client.delete_schedule(schedule_name)
    print(response)


def describe_schedule(args):
  """Describe the schedule."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.describe_schedule(args.schedule_name, args.org_id)
  else:
    response = client.describe_schedule(args.schedule_name)

  if not isinstance(response, str):
    print_schedule_info(response)
  else:
    print("response: {}".format(response))

def start_schedule(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.start_schedule(args.schedule_name, args.org_id)
  else:
    response = client.start_schedule(args.schedule_name)
  print(response)

def stop_schedule(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.stop_schedule(args.schedule_name, args.org_id)
  else:
    response = client.stop_schedule(args.schedule_name)
  print(response)

def create_schedule(args):
  return create_or_update_schedule(args, True)


def update_schedule(args):
  return create_or_update_schedule(args, False)


def create_or_update_schedule(args, is_create=True):
  """Submit the job."""

  args_dict = vars(args)
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  if not args.schedule_name:
    exit_as_error("ERROR: parameters schedule_name is necessary.")
    return

  schedule = Schedule(args.schedule_name)

  if 'resource_name' not in args:
    raise ValueError('ERROR: resource_name is necessary')

  if args.resource_type:
    schedule.resource_type = args.resource_type

  if args.resource_name:
    schedule.resource_name = args.resource_name
  elif is_create:
    raise ValueError('ERROR: resource_name is necessary')

  if args.cron_param:
    schedule.cron_param = args.cron_param
  elif is_create:
    raise ValueError('ERROR: cron_param is necessary')


  if args.success_history_limit:
    schedule.success_history_limit = args.success_history_limit
  # for hdfs
  if args.failed_history_limit:
    schedule.failed_history_limit = args.failed_history_limit
  if args.suspend:
    schedule.suspend = args.suspend
  if args.concurrency_policy:
    schedule.concurrency_policy = args.concurrency_policy
  if args.image_name:
    schedule.image_name = args.image_name

  json_data = schedule.get_json_data()
  if is_create:
    response = client.create_schedule(json_data)
  else:
    response = client.update_schedule(json_data, args.schedule_name)

  if not isinstance(response, str):
    print_schedule_info(response)
  else:
    print("response: {}".format(response))


def print_ceph_list(response, args):
  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    print("{:16} {:16} {:16} {:16} {:16} {:32}".format(
      "ORG ID", "ORG NAME", "CEPH_NAME", "CAPACITY", "STATUS", "CREATED"))
    for ceph in response:
      print("{:16} {:16} {:16} {:16} {:16} {:32}".format(ceph["org_id"], 
                                                         ceph["org_name"], 
                                                         ceph["ceph_name"], 
                                                         ceph["capacity"],
                                                         color_util.colorize_state(ceph["status"]),
                                                         ceph["create_time"]))
  else:
    print("{:16} {:16} {:16} {:32}".format(
      "CEPH_NAME", "CAPACITY", "STATUS", "CREATED"))
    for ceph in response:
      print("{:16} {:16} {:16} {:32}".format(ceph["ceph_name"], 
                                            ceph["capacity"],
                                            color_util.colorize_state(ceph["status"]),
                                            ceph["create_time"]))

def print_ceph_info(ceph):
  """Print ceph in customized format.

  Args:
    ceph: The dictionary of response ceph data.
  """
  print("{:16} {}".format("Org id:", ceph["org_id"]))
  print("{:16} {}".format("Org name:", ceph["org_name"]))
  print("{:16} {}".format("Ceph name:", ceph["ceph_name"]))
  print("{:16} {}".format("Capacity:", ceph["capacity"]))
  print("{:16} {}".format("Status:", ceph.get("status")))
  print("{:16} {}".format("Create time:", ceph["create_time"]))


def create_ceph(args):
  """Create a ceph volume."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  ceph = CephService(args.ceph_name, args.capacity)

  response = client.create_ceph_service(ceph)
  if not isinstance(response, str):
    print_ceph_info(response)
  else:
    print("response: {}".format(response))


def describe_ceph(args):
  """Describe the ceph volume."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.describe_ceph_service(args.ceph_name, 
                                            args.org_id)
  else:
    response = client.describe_ceph_service(args.ceph_name)
  if not isinstance(response, str):
    print_ceph_info(response)
  else:
    print("response: {}".format(response))


def delete_ceph(args):
  """Delete the ceph volume(s)."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    for ceph_name in args.ceph_names:
      response = client.delete_ceph_service(ceph_name=ceph_name, org_id=args.org_id, force=args.force)
      print(response)
  else:
    for ceph_name in args.ceph_names:
      response = client.delete_ceph_service(ceph_name=ceph_name, org_id=None, force=args.force)
      print(response)


def get_ceph_events(args):
  """Get events of the ceph volume."""

  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  response = client.get_ceph_service_events(args.ceph_name)
  # TODO format ceph events
  print("response: {}".format(response))


def list_cephs(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    response = client.list_ceph_services(constant.CLOUDML_ALL_ORG_PARAMETER)
  else:
    response = client.list_ceph_services()
  if not isinstance(response, str):
    print_ceph_list(response, args)
  else:
    print("response: {}".format(response))


def list_secret_services(args):
  """List secret_services."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      response_secret = client.list_secret_services(
          constant.CLOUDML_ALL_ORG_PARAMETER)
    else:
      response_secret = client.list_secret_services(args.org_id)
  else:
    response_secret = client.list_secret_services()

  if not isinstance(response_secret, str):
    print_secret_list(response_secret, args)
  else:
    print("response: {}".format(response_secret))


def print_secret_list(response_secrets, args):
  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    print("{:16} {:16} {:32} {:32}".format(
      "ORG ID", "ORG NAME", "SECRET_NAME", "CREATED"))
    for secret in response_secrets:
      print("{:16} {:16} {:32} {:32}".format(secret["org_id"], secret["org_name"],
                                             secret["secret_name"], secret["create_time"]))
  else:
    print("{:32} {:32}".format(
      "SECRET_NAME", "CREATED"))
    for secret in response_secrets:
      print("{:32} {:32}".format(secret["secret_name"], secret["create_time"]))


def create_secret_service(args):
  """create the secret_service."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  with open(args.file_path, 'rb') as f:
    # TODO: Check file format and verify the items
    try:
      data = base64.b64encode(f.read())
    except Exception as e:
      exit_as_error("ERROR: secret file({}) is not valid: {}".format(args.file_path, e))
      return

  secret = SecretService(args.secret_name, data)

  response = client.create_secret_service(secret)
  if not isinstance(response, str):
    print_secret_info(response)
  else:
    print("response: {}".format(response))


def describe_secret_service(args):
  """Describe the secret_service."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    response = client.describe_secret_service(args.secret_name,
                                              args.org_id)
  else:
    response = client.describe_secret_service(args.secret_name)
  if not isinstance(response, str):
    print_secret_info(response)
  else:
    print("response: {}".format(response))


def delete_secret_service(args):
  """Delete the secret_service(s)."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args:
    for secret_name in args.secret_names:
      response = client.delete_secret_service(secret_name, args.org_id)
      print(response)
  else:
    for secret_name in args.secret_names:
      response = client.delete_secret_service(secret_name)
      print(response)


def list_namespaces(args):
  """List namespaces."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  response = client.list_namespaces()

  if not isinstance(response, str):
    print_namespace_list(response, args)
  else:
    print("response: {}".format(response))


def print_namespace_list(response_namespaces, args):
  print("{:32} {:32} {:32}".format(
    "NAMESPACE", "OWER_EMAIL", "DESCRIPTION"))
  for ns in response_namespaces:
    print("{:32} {:32} {:32}".format(ns["name"], ns["owner_email"],  ns.get("description", "")))


def create_namespace(args):
  """create the namespace."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  ns = NamespaceService(args.name,
                        args.owner_email,
                        args.description)

  response = client.create_namespace(ns)
  if not isinstance(response, str):
    print_namespace_info(response)
  else:
    print("response: {}".format(response))


def update_namespace(args):
  """update the namespace."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  ns = NamespaceService(args.name,
                        args.owner_email,
                        args.description)

  response = client.update_namespace(ns)
  if not isinstance(response, str):
    print_namespace_info(response)
  else:
    print("response: {}".format(response))


def print_namespace_info(ns):
  """Print namespace in customed format.

  Args:
    ns: The dictionary of response namespace data.
  """
  print("{:16} {}".format("Name:", ns["name"]))
  print("{:16} {}".format("Owner Email:", ns["owner_email"]))
  print("{:16} {}".format("Description:", ns.get("description", "")))


def describe_namespace(args):
  """Describe the namespace."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  response = client.describe_namespace(args.name)
  if not isinstance(response, str):
    print_namespace_info(response)
  else:
    print("response: {}".format(response))


def delete_namespace(args):
  """Delete the namespace(s)."""
  confirm = raw_input("Warning: This deletes everything under the namespace!\nDo you want to continue?[y/n]")
  if confirm == "y" or confirm == "yes":
    try:
      client = CloudMlClient()
    except Exception as e:
      exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
      return

    for ns in args.names:
      response = client.delete_namespace(ns)
      print(response)


def list_namespace_quota(args):
  """List namespace quotas."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  response = client.list_namespace_quotas()

  if not isinstance(response, str):
    print_namespace_quota_list(response, args)
  else:
    print("response: {}".format(response))


def print_namespace_quota_list(response_namespace_quotas, args):
  print("{:32} {:24} {:24} {:24}".format(
    "NAMESPACE", "CPU / USED", "MEM / USED", "GPU / USED"))
  for quota in response_namespace_quotas:
    print("{:32} {:24} {:24} {:24}".format(quota["name"],
                                           "".join([quota["cpu"], " / ", quota["cpu_used"]]),
                                           "".join([quota["memory"], " / ", quota["memory_used"]]),
                                           "".join([quota["gpu"], " / ", quota["gpu_used"]])
                                           ))


def create_namespace_quota(args):
  """create the namespace quota."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  print("args: ", args)

  ns_quota = NamespaceQuotaService(args.name,
                                   args.cpu,
                                   args.memory,
                                   args.gpu)

  response = client.create_namespace_quota(ns_quota)
  if not isinstance(response, str):
    print_namespace_quota_info(response)
  else:
    print("response: {}".format(response))


def update_namespace_quota(args):
  """update the namespace quota."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  print("args: ", args)

  ns_quota = NamespaceQuotaService(args.name,
                                   args.cpu,
                                   args.memory,
                                   args.gpu)

  response = client.update_namespace_quota(ns_quota)
  if not isinstance(response, str):
    print_namespace_quota_info(response)
  else:
    print("response: {}".format(response))


def print_namespace_quota_info(ns):
  """Print namespace quota in customed format.

  Args:
    ns: The dictionary of response namespace quota data.
  """
  print("{:16} {}".format("Name:", ns["name"]))
  print("{:16} {} / {}".format("CPU / Used:", ns["cpu"], ns["cpu_used"]))
  print("{:16} {} / {}".format("MEM / Used:", ns["memory"], ns["memory_used"]))
  print("{:16} {} / {}".format("GPU / Used:", ns["gpu"], ns["gpu_used"]))


def describe_namespace_quota(args):
  """Describe the namespace quota."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  response = client.describe_namespace_quota(args.name)
  if not isinstance(response, str):
    print_namespace_quota_info(response)
  else:
    print("response: {}".format(response))


def list_namespace_user(args):
  """List namespace users."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  response = client.list_namespace_users(args.namespace)

  if not isinstance(response, str):
    print_namespace_user_list(response)
  else:
    print("response: {}".format(response))


def print_namespace_user_list(response_namespace_users):
  print("{:32} {:32}".format(
    "NAMESPACE", "USER ID"))
  for ns_user in response_namespace_users:
    print("{:32} {:32}".format(ns_user["namespace"],
                               ns_user["user_id"]))

def add_namespace_user(args):
  """add the namespace user."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  for user_id in args.user_ids:
    ns_user = NamespaceUserService(args.namespace, user_id)

    response = client.add_namespace_user(ns_user)
    if not isinstance(response, str):
      print_namespace_user_info(response)
    else:
      print("response: {}".format(response))


def remove_namespace_user(args):
  """remove the namespace user."""
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return

  for user_id in args.user_ids:
    ns_user = NamespaceUserService(args.namespace, user_id)

    response = client.remove_namespace_user(ns_user)
    print("response: {}".format(response))


def print_namespace_user_info(ns):
  """Print namespace user in customed format.

  Args:
    ns: The dictionary of response namespace user data.
  """
  print("{:16} {}".format("Namespace:", ns["namespace"]))
  print("{:16} {}".format("User ID:", ns["user_id"]))



def list_all(args):
  """List all resources."""

  print("List all train jobs:")
  list_jobs(args)
  print("\nList all model services:")
  list_models(args)
  print("\nList all dev environments:")
  list_dev_envs(args)
  print("\nList all tensorboard services:")
  list_tensorboard_services(args)
  print("\nList all pipelines:")
  list_pipelines(args)
  print("\nList all cephs:")
  list_cephs(args)

def exit_as_error(message, error_code=-1, is_os_exit=False):
  print(message)
  if is_os_exit:
    # os exit can not be catched
    os._exit(error_code)
  else:
    sys.exit(error_code)

def list_cluster_available_resources(args):
  try:
    client = CloudMlClient()
  except Exception as e:
    exit_as_error("ERROR: Failed to init CloudML Client: {}".format(e))
    return
  if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
    response = client.list_cluster_resources(constant.CLOUDML_ALL_ORG_PARAMETER)
  else:
    response = client.list_cluster_resources()
  if not isinstance(response, str):
    print_resources_list(response)
  else:
    print("response: {}".format(response))

def print_resources_list(data):
  print("{:32} {:32} {:32}".format("Available cpu","Available memory", "Available gpu"))
  for item in data:
    print("{:32} {:32} {:32}".format(str(item["available_cpu"]), item["available_mem"], str(item["available_gpu"])))

def get_cur_time():
  localtime = time.localtime(time.time())
  return str(localtime.tm_mon).zfill(2) + str(localtime.tm_mday).zfill(2) + str(localtime.tm_hour).zfill(2) + str(localtime.tm_min).zfill(2)
