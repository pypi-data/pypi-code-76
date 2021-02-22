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
# valueations under the License.
import json
import re
from datetime import datetime
import time
import os
import errno
import tarfile
import netaddr
import tempfile

from cloud_ml_sdk.client import CloudMlClient
from cloud_ml_sdk.client import CLOUDML_UPLOAD_PACKAGE_DIR

from . import constant

kube_resource_name_regex = "[a-z0-9]([-a-z0-9]*[a-z0-9])?$"
kube_resource_name_regex_pattern = re.compile(kube_resource_name_regex)


def check_kube_resource_name_regex(resource_name):
  if kube_resource_name_regex_pattern.match(resource_name):
    return True
  else:
    return False


def check_cpu_value(value):
  if value != None:
    if not isinstance(value, str):
      raise ValueError("cpu value must be a string!")
    if not value.replace(".", "", 1).isdigit():
      raise ValueError("cpu value must be a number!")
    digits = value.split(".")
    if len(digits) == 2 and len(digits[1]) > constant.QUOTA_ACCURACY_PLACE:
      raise Exception(
          "The value of cpu accurate to two decimal places, for example: {}".format(
              round(
                  float(value), constant.QUOTA_ACCURACY_PLACE)))
  return value


def check_memory_value(value):
  if value != None:
    if not isinstance(value, str):
      raise ValueError("memory value must be a string")
    unit = value[-1:]
    float_value = value[:-1]
    if unit not in constant.CLOUDML_MEMORY_UNITS:
      raise ValueError("memory value unit must be one of %s!" %
                       constant.CLOUDML_MEMORY_UNITS)
    if not float_value.replace(".", "", 1).isdigit():
      raise ValueError("memory value must be a number!")
    digits = float_value.split(".")
    if len(digits) == 2 and len(digits[1]) > constant.QUOTA_ACCURACY_PLACE:
      raise Exception(
          "The value of memory accurate to two decimal places, for example: {}".format(
              round(
                  float(float_value), constant.QUOTA_ACCURACY_PLACE)))
  return value


def check_gpu_value(value):
  if value != None:
    if not (isinstance(value, str) and value.isdigit() and int(value) >= 0):
      raise ValueError("gpu value must be a string for nonnegative integer!")
    value = int(value)
  return value


def check_distributed_count(value):
  if value != None:
    if not (isinstance(value, str) and value.isdigit() and int(value) > 0):
      raise ValueError("Distributed task count must be a string for positive integer!")
    value = int(value)
  return value

def check_network_port(port):
  try:
    p = int(port)
    if p < constant.DEV_PROXY_MIN_CONTAINER_PORT or p > constant.DEV_PROXY_MAX_CONTAINER_PORT:
      raise ValueError("Network port should be in the range of [{}, {}]".format(constant.DEV_PROXY_MIN_CONTAINER_PORT,constant.DEV_PROXY_MAX_CONTAINER_PORT))
  except:
    raise ValueError("Network port should be in the range of [{}, {}]".format(constant.DEV_PROXY_MIN_CONTAINER_PORT,constant.DEV_PROXY_MAX_CONTAINER_PORT))
  return p

def check_network_whitelist(white):
  whitelist = white.strip().split(" ")
  for i in whitelist:
    if not check_cidr(i):
      raise ValueError("Network whitelist should be in CIDR format")
  return whitelist

def check_cidr(cidr):
  try:
    if cidr == None or not isinstance(cidr, str) or cidr.count(".") != 3:
      return False
    netaddr.IPNetwork(cidr)
    return True
  except Exception as e:
    return False

# TODO change train model
def validate_and_get_fds_uri(uri, field_name = 'code_uri'):
  """Function for setting code_uri.

     Args:
       value: String type value that is going to be set to code_uri. Which
              cannot be empty. code_uri must be a valid local tar.gz file path
              or a valid fds tar.gz path

     Raises:
       ValueError: If value is in one of he following cases: not a str instance;
                   not a valid fds path; not a valid local path or file not exist.
     """
  if not isinstance(uri, str):
    raise ValueError("%s must be a string!" % field_name)

  if uri.startswith("fds://"):
    fds_client = CloudMlClient().get_fds_client()
    bucket = uri.split('/', 3)[2]
    if fds_client.does_object_exists(bucket, uri.split('/', 3)[-1]):
      to_return = uri
    else:
      raise ValueError("Can't find file " + uri + " in fds directory!")
  else:
    if not os.path.isfile(uri):
      raise ValueError("Can't find file " + uri + " in your local directory!")
    # auto upload tar.gz file if a local directory is given
    else:
      try:
        to_return = upload_package(uri)
      except ValueError as e:
        raise ValueError(e.message)

  return to_return


def validate_fds_dir(value, field_name="module"):
  if value is None:
    return value
  if not isinstance(value, str):
    raise ValueError("%s must be a string!" % field_name)
  if value == "":
    raise ValueError("%s cannot be None!" % field_name)
  # TODO add check logic
  '''
  fds_client = CloudMlClient().get_fds_client()
  bucket = value.split('/', 3)[2]
  if fds_client.does_object_exists(bucket, value.split('/', 3)[-1]):
    raise ValueError("Can't find directory " + value + " in fds!")
  '''
  return value


def validate_json_str(value, field_name="stages"):
  if value is None:
    return value
  if not isinstance(value, str):
    raise ValueError("%s must be a string!" % field_name)
  if len(value) > 0:
    # validate if the value is json format
    try:
      json.loads(value)
    except ValueError as e:
      raise ValueError("%s must be json format" % field_name)
  return value
def compression_dir(target_dir, output_path):
    try:
      with tarfile.open(output_path, "w:gz") as tar:
        tar.add(target_dir, arcname=os.path.basename(target_dir))
    except Exception as e:
      raise ValueError("Compression directory: {} got error: {}".format(target_dir, e))

def remove_file(target_path):
    try:
      os.remove(target_path)
    except OSError as e:
      if e.errno != errno.ENOENT:
        raise ValueError("Deleting file: {} got error: {}".format(target_path, e))

def tar_and_upload_package(local_path):
  """Tar user's package dir and upload to user's default bucket

  Args:
    local_path: local dir of user's train model.

  Returns:
    return the fds location that is newly created to store user's .tar.gz package.
  """
  target_dir = os.path.abspath(local_path)
  basename = os.path.basename(target_dir)
  output_path = os.path.join(tempfile.gettempdir(), basename + ".cloudml.tar.gz")

  compression_dir(target_dir, output_path)
  fds_path = upload_package(output_path)
  remove_file(output_path)

  return fds_path


def upload_package(local_path):
  """Upload user's package to user's default bucket

  Args:
    local_path: local path of user's package(tar.gz package).

  Returns:
    return the fds location that is newly created to store user's .tar.gz package.
  """
  cloudml_client = CloudMlClient()
  bucket = None
  if "CLOUDML_DEFAULT_FDS_BUCKET" in os.environ:
    bucket = os.environ["CLOUDML_DEFAULT_FDS_BUCKET"]
  else:
    config_data = cloudml_client.get_config_data()
    if config_data and "cloudml_default_fds_bucket" in config_data:
      bucket = config_data["cloudml_default_fds_bucket"]
  
  fds_client = cloudml_client.get_fds_client()
  if bucket:
    if not fds_client.does_bucket_exist(bucket):
        raise ValueError("Can't find " + bucket + " bucket in fds server! Please check again!")
  else:
    # upload to Cloud-ML shared fds bucket-cloudmlusers, https://jira.n.xiaomi.com/browse/CLOUDML-10
    bucket = constant.CLOUDML_SHARED_BUCKET
  
  try:
    with open(local_path, 'rb') as f:
      tag = datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
      file_name = local_path.split('/')[-1][:-7] + '_' + tag + '.tar.gz'
      data = f.read()
      res = fds_client.put_object(bucket, CLOUDML_UPLOAD_PACKAGE_DIR + file_name, data)
      # NOTE(xychu): fds always using '/' as sep
      return 'fds://' + bucket + "/" + CLOUDML_UPLOAD_PACKAGE_DIR + file_name
  except Exception as e:
    raise ValueError("Upload package got error: ", e)


def validate_and_get_trainer_uri(value):
  if not isinstance(value, str):
    raise ValueError("trainer_uri must be a string!")

  if value.startswith("fds://"):
    fds_client = CloudMlClient().get_fds_client()
    bucket = value.split('/', 3)[2]
    if fds_client.does_object_exists(bucket, value.split('/', 3)[-1]):
      to_return = value
    else:
      raise ValueError("Can't find file " + value + " in fds directory!")
  else:
    # auto upload tar.gz file if a local file is given
    if os.path.isfile(value):
      try:
        to_return = upload_package(value)
      except ValueError as e:
        raise ValueError(e.message)
    # auto compress and upload tar.gz file if a local directory is given
    elif os.path.isdir(value):
      try:
        to_return = tar_and_upload_package(value)
      except Exception as e:
        raise ValueError("Tar and upload package got error: ", e)
    else:
      raise ValueError("Invalid trainer_uri. %s is not a local file or directory or fds path." % value)

  return to_return
