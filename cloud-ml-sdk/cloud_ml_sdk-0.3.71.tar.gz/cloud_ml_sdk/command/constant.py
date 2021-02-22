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

SDK_NAME = "cloud_ml_sdk"
DEFAULT_CLOUDML_API_ENDPOINT = "https://cnbj3-cloud-ml.api.xiaomi.net"
CLOUDML_ALL_ORG_PARAMETER = "-1"

INF_JOB_COUNT = "-1"

INF_TOTAL_MEMORY_QUOTA = "-1.0K"
INF_TOTAL_CPU_QUOTA = "-1.0"
INF_TOTAL_GPU_QUOTA = "-1"

PIPELINE_STATE_COMPLETED = "completed"
PIPELINE_STATE_FAILED = "failed"
JOB_STATE_COMPLETED = "completed"
MODEL_STATE_RUNNING = "running"
DEV_ENV_STATE_RUNNING = "running"
JOB_STATE_FAILED = "failed"
JOB_STATE_MODELSERVED = "modelserved"

JOB_WATCH_INTERVAL = 3
PIPELINE_WATCH_INTERVAL = 3
ARGO_COMMAND_WAIT = 3

ENABLE_GPU_TYPE_SELECT = False
GPULIST = ["m40", "p40", "k40", "p4", "v100"]

CLOUDML_MEMORY_UNITS = ["K", "M", "G"]
QUOTA_ACCURACY_PLACE = 2
PRI_RANK = ["1", "2", "3"]

DEV_PROXY_PROTOCOL = {8888: "JUPYTER", 22: "TCP"}
DEV_PROXY_MIN_CONTAINER_PORT = 1
DEV_PROXY_MAX_CONTAINER_PORT = 65535

PIPELINE_TYPE_TRAINING = "train"
PIPELINE_TYPE_MODELSERVICE = "model"
PIPELINE_TYPE_TENSORBOARD = "tensorboard"

PIPELINE_TYPE_NAME_MAP = {
  PIPELINE_TYPE_TRAINING: "job_name",
  PIPELINE_TYPE_MODELSERVICE: "model_name",
  PIPELINE_TYPE_TENSORBOARD: "tensorboard_name"
}

CONFIG_PATH = ".config/xiaomi/"
CONFIG_FILENAME = "config"
DEFAULT_CONFIG_CONTEXT = "default_config_context"
CLOUDML_CONFIG_KEY = "xiaomi_cloudml"

SECRET_KEYTAB_KEY = "keytab"
