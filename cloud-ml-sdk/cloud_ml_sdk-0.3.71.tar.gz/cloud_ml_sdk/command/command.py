#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

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

import argcomplete
import argparse
import logging
import pkg_resources
import sys

sys.path.append("../../")

from . import constant
from . import util

logging.basicConfig(level=logging.DEBUG)


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument(
      "-v",
      "--version",
      action="version",
      version=pkg_resources.require(constant.SDK_NAME)[0].version,
      help="Show version")

  parser.add_argument(
      "-k", "--context", dest="config_context_name", action=util.SetConfigContextEnv,
      help="The cloudml config context name, available values can be listed by: cloudml config show")

  main_subparser = parser.add_subparsers(dest="command_group", help="Commands")

  # Deprecated `cloudml init`, use `cloudml config init` instead
  init_parser = main_subparser.add_parser("init", help="[DEPRECATED] Init cloudml config")
  init_parser.set_defaults(func=util.deprecated_init_config)

  # subcommand: config
  config_parser = main_subparser.add_parser("config", help="Commands about cloudml config")

  config_subparser = config_parser.add_subparsers(
      dest="config_command", help="Subcommands of config")

  # subcommand of config: init
  config_init_parser = config_subparser.add_parser("init", help="Init cloudml config")
  config_init_parser.set_defaults(func=util.init_config)

  # subcommand of config: show
  config_show_parser = config_subparser.add_parser("show", help="Show cloudml config")
  config_show_parser.set_defaults(func=util.show_config)

  # subcommand of config: set default config context
  config_set_parser = config_subparser.add_parser(
      "set_default", help="Set default cloudml config context",
      description="Get potential `config_context_name` from config via: cloudml config show")
  config_set_parser.add_argument("config_context_name", help="The name of the default config context")
  config_set_parser.set_defaults(func=util.set_default_config)

  # subcommand of config: delete cluster config
  config_delete_parser = config_subparser.add_parser("delete", help="Delete cloudml config context")
  config_delete_parser.add_argument("config_context_names", metavar="config_context_name", nargs="+", help="The name of the config context")
  config_delete_parser.set_defaults(func=util.delete_config_context)

  # subcommand of config: fds
  config_fds_parser = config_subparser.add_parser("fds", help="Set fds config")
  config_fds_parser.set_defaults(func=util.fds_config)

  # subcommand of config: hdfs
  config_hdfs_parser = config_subparser.add_parser("hdfs", help="Set hdfs config")
  config_hdfs_parser.set_defaults(func=util.hdfs_config)

  org_id_parser = main_subparser.add_parser(
      "org_id", help="Get org_id by access_key and secret_key")
  org_id_parser.set_defaults(func=util.get_org_id)

  #subcommand :hptuning
  hptuning_parser = main_subparser.add_parser("hp", help="Commands about hptuning")
  hptuning_subparser = hptuning_parser.add_subparsers(
      dest="hp_command", help="Subcommands of hptuning")

  # subcommand of hptunings: submit
  hptuning_submit_parser = hptuning_subparser.add_parser("submit", help="Submit hptuning")
  hptuning_submit_parser.add_argument(
      "-f",
      "--filename",
      dest="filename",
      help="The json file contains the hptuning task msg")
  hptuning_submit_parser.set_defaults(func=util.submit_hptuning)

  # subcommand of hptunings: delete
  hptuning_delete_parser = hptuning_subparser.add_parser(
      "delete", help="Delete the hptuning(s)")
  hptuning_delete_parser.add_argument("hp_names", metavar="hp_name", nargs="+", help="The name of the hptuning")
  hptuning_delete_parser.set_defaults(func=util.delete_hp)

  # subcommand of hptunings: list
  hptuning_list_parser = hptuning_subparser.add_parser("list", help="List hptunings")
  hptuning_list_parser.set_defaults(func=util.list_hp)

  # subcommand of hptunings: describe
  hptuning_describe_parser = hptuning_subparser.add_parser(
      "describe", help="Describe hp job")
  hptuning_describe_parser.add_argument("hp_name", help="The hp job to describe")
  hptuning_describe_parser.set_defaults(func=util.describe_hp_job)

  # subcommand of hptunings: get trials
  hptuning_trials_parser = hptuning_subparser.add_parser("trials", help="get trials")
  hptuning_trials_parser.add_argument("hp_name",
                                      help="the hptuning job the trials belong to")
  hptuning_trials_parser.set_defaults(func=util.get_trials)

  # subcommand of hptunings: get trial log
  hptuning_trial_log_parser = hptuning_subparser.add_parser("logs", help="get log of the trial")

  hptuning_trial_log_parser.add_argument("hp_name", help="the hptuning job the trials belong to")

  hptuning_trial_log_parser.add_argument("-ti",
                                      "--trial_id",
                                      dest="trial_id",
                                      help="the log of the trial(pod)")
  hptuning_trial_log_parser.add_argument("-f", "--follow", action="store_true",
                                help="Follow the log stream of the pod. Defaults to false.")
  hptuning_trial_log_parser.add_argument("-n", "--lines", type=int, help="The last number of lines to show.")
  hptuning_trial_log_parser.set_defaults(func=util.get_trial_log)

  #subcommand of hp_jobs: events
  hptuning_events_parser = hptuning_subparser.add_parser(
      "events", help="Get the events of the train job")
  hptuning_events_parser.add_argument("hp_name", help="The name of the train job")
  hptuning_events_parser.set_defaults(func=util.get_hp_job_events)
  

  # subcommand of jobs: metrics
  hptuning_metrics_parser = hptuning_subparser.add_parser(
      "metrics", help="Get the metrics of the hp job")
  hptuning_metrics_parser.add_argument("hp_name", help="The hp job to get the logs")
  hptuning_metrics_parser.set_defaults(func=util.get_hp_metrics)

  # subcommand: jobs
  jobs_parser = main_subparser.add_parser("jobs", help="Commands about jobs")
  jobs_subparser = jobs_parser.add_subparsers(
      dest="job_command", help="Subcommands of jobs")

  # subcommand of jobs: list
  jobs_list_parser = jobs_subparser.add_parser("list", help="List jobs")
  jobs_list_parser.add_argument("-o", "--output", dest="output", help="The output form : now only support: wide(node the task assigned to)")
  jobs_list_parser.set_defaults(func=util.list_jobs)

  # subcommand of jobs: submit
  jobs_submit_parser = jobs_subparser.add_parser("submit", help="Submit job")
  jobs_submit_parser.add_argument(
      "-f",
      "--filename",
      dest="filename",
      help="The json file contains the job task msg")

  jobs_submit_parser.add_argument(
      "-n", "--job_name", dest="job_name", help="The job name")
  jobs_submit_parser.add_argument(
      "-m", "--module_name", dest="module_name", help="The module name")
  jobs_submit_parser.add_argument(
      "-u", "--trainer_uri", dest="trainer_uri",
      help="The trainer uri, support `fds://` or local tar.gz file path or even local directory`. " +
           "e.g. ./ or /path/to/my/ml_project. " +
           "NOTE: when using local directory, `setup.py` or `requirements.txt` in the top level of the target directory " +
           "will be used to install any extra dependencies.")
  jobs_submit_parser.add_argument(
      "-a", "--job_args", dest="job_args", help="The string of args")
  jobs_submit_parser.add_argument(
      "-fe", "--fds_endpoint", dest="fds_endpoint", help="The fds endpoint use")
  jobs_submit_parser.add_argument(
      "-fb", "--fds_bucket", dest="fds_bucket", help="The fds bucket to mount to /fds")
  #for hdfs
  jobs_submit_parser.add_argument(
      "-hka", "--hdfs_krb_account", type=str,dest="hdfs_krb_account", help="The kerberos account"
  )
  jobs_submit_parser.add_argument(
      "-hkp", "--hdfs_krb_password", type=str,dest="hdfs_krb_password", help="The kerberos password"
  )
  jobs_submit_parser.add_argument(
      "-hkt", "--hdfs_krb_keytab", type=str, dest="hdfs_krb_keytab", help="The kerberos keytab secret name"
  )
  jobs_submit_parser.add_argument(
      "-he", "--hdfs_endpoint", type=str,dest="hdfs_endpoint", help="The hadoop path to mount to /hdfs"
  )
  jobs_submit_parser.add_argument(
      "-c",
      "--cpu_limit",
      dest="cpu_limit",
      help="The CPU limit with unit core")
  jobs_submit_parser.add_argument(
      "-M",
      "--memory_limit",
      dest="memory_limit",
      help="The memory limit with unit K, M or G")
  jobs_submit_parser.add_argument(
      "-g", "--gpu_limit", dest="gpu_limit", help="The number of GPU limit")
  gpu_type_help = "select gpu type from ({})".format("/".join(constant.GPULIST))
  if not constant.ENABLE_GPU_TYPE_SELECT:
    gpu_type_help = "[DEPRECATED] " + gpu_type_help
  jobs_submit_parser.add_argument(
    "-gt",
    "--gpu_type",
    dest="gpu_type",
    help=gpu_type_help
  )
  jobs_submit_parser.add_argument(
      "-p",
      "--ps_count",
      dest="ps_count",
      help="The number of ps for distributed training")
  jobs_submit_parser.add_argument(
      "-w",
      "--worker_count",
      dest="worker_count",
      help="The number of worker for distributed training")
  jobs_submit_parser.add_argument(
      "-D",
      "--distributed",
      action="store_true",
      help="General distributed train")
  jobs_submit_parser.add_argument(
      "-R",
      "--enable_rank",
      dest = "enable_rank",
      action = "store_true",
      help = "Create priority high train"
  )
  jobs_submit_parser.add_argument(
      "-d", "--docker_image", dest="docker_image", help="The docker image")
  jobs_submit_parser.add_argument(
      "-dc",
      "--docker_command",
      dest="docker_command",
      help="The docker command")
  jobs_submit_parser.add_argument(
      "-F",
      "--framework",
      dest="framework",
      help="The framework of machine learning")
  jobs_submit_parser.add_argument(
      "-V",
      "--framework_version",
      dest="framework_version",
      help="The version of the framework")
  jobs_submit_parser.add_argument(
      "-vt", "--volume_type", dest="volume_type", help="The volume type")
  jobs_submit_parser.add_argument(
      "-vp", "--volume_path", dest="volume_path", help="The volume path")
  jobs_submit_parser.add_argument(
      "-mp", "--mount_path", dest="mount_path", help="The mount type")
  jobs_submit_parser.add_argument(
      "-mro",
      "--mount_read_only",
      dest="mount_read_only",
      help="Whether mount read only or not")
  jobs_submit_parser.add_argument(
      "-pc",
      "--prepare_command",
      dest="prepare_command",
      help="The prepare command")
  jobs_submit_parser.add_argument(
      "-fc",
      "--finish_command",
      dest="finish_command",
      help="The finish command")
  jobs_submit_parser.add_argument(
      "-W", "--watch", action="store_true", help="Watch the status of job")
  jobs_submit_parser.add_argument(
      "-nsk",
      "--node_selector_key",
      dest="node_selector_key",
      help="The node selector key")
  jobs_submit_parser.add_argument(
      "-nsv",
      "--node_selector_value",
      dest="node_selector_value",
      help="The node selector value")
  jobs_submit_parser.add_argument(
      "-cs",
      "--cluster_spec",
      dest="cluster_spec",
      help='The cluster specific, e.g. --cluster_spec=\'{"ps": {"count": 1, "memory_limit": "1G", "task_args": "--num_gpus=0", "gpu_limit": 0, "cpu_limit": "1"}, "chief": {"count": 1, "memory_limit": "1G", "task_args": "--num_gpus=0", "gpu_limit": 0, "cpu_limit": "1"}, "worker": {"count": 1, "memory_limit": "1G", "task_args": "--num_gpus=0", "gpu_limit": 0, "cpu_limit": "1"}}\'')
  jobs_submit_parser.add_argument(
      "-sv",
      "--save_mode",
      dest="save_mode",
      help="Save job, don't run",
      action='store_true')
  jobs_submit_parser.add_argument(
      "-argo",
      "--argo_mode",
      dest="argo_mode",
      help="mark it a argo job",
      action='store_true')
  jobs_submit_parser.add_argument(
      "-tl",
      "--tensorboard_logdir",
      dest="tensorboard_logdir",
      help="Tensorboard logdir of the job")
  jobs_submit_parser.add_argument(
      "-mn",
      "--model_name",
      dest="model_name",
      help="model name (must be initial status) of the job")
  jobs_submit_parser.add_argument(
    "-mv",
    "--model_version",
    dest="model_version",
    help="model version(must be initial status) of the job")

  jobs_submit_parser.set_defaults(func=util.submit_job)

  # subcommand of jobs: describe
  jobs_describe_parser = jobs_subparser.add_parser(
      "describe", help="Describe job")
  jobs_describe_parser.add_argument("job_name", help="The job to describe")
  jobs_describe_parser.set_defaults(func=util.describe_job)

  # subcommand of jobs: logs
  jobs_logs_parser = jobs_subparser.add_parser(
      "logs", help="Get the logs of the job")
  jobs_logs_parser.add_argument("-f", "--follow", action="store_true",
                                help="Follow the log stream of the pod. Defaults to false.")
  jobs_logs_parser.add_argument("-n", "--lines", type=int, help="The last number of lines to show.")
  jobs_logs_parser.add_argument("job_name", help="The job to get the logs")
  jobs_logs_parser.set_defaults(func=util.get_job_logs)

  # subcommand of jobs: metrics
  jobs_metrics_parser = jobs_subparser.add_parser(
      "metrics", help="Get the metrics of the job")
  jobs_metrics_parser.add_argument("job_name", help="The job to get the logs")
  jobs_metrics_parser.set_defaults(func=util.get_job_metrics)

  # subcommand of jobs: hp
  jobs_hp_parser = jobs_subparser.add_parser(
      "hp", help="Get the hyperparameters data of the job")
  jobs_hp_parser.add_argument("job_name", help="The job name")
  jobs_hp_parser.set_defaults(func=util.get_job_hyperparameters_data)

  # subcommand of jobs: delete
  jobs_delete_parser = jobs_subparser.add_parser(
      "delete", help="Delete the job(s)")
  jobs_delete_parser.add_argument("-n", "--is_cluster_name", action="store_true",
                                  help="Delete the cluster job by cluster name, Defaults to false.")
  jobs_delete_parser.add_argument("job_names", metavar="job_name", nargs="+", help="The name of the job")
  jobs_delete_parser.set_defaults(func=util.delete_job)

  # subcommand of jobs: events
  jobs_events_parser = jobs_subparser.add_parser(
      "events", help="Get the events of the train job")
  jobs_events_parser.add_argument("job_name", help="The name of the train job")
  jobs_events_parser.set_defaults(func=util.get_train_job_events)

  # subcommand of jobs: start
  jobs_start_parser = jobs_subparser.add_parser(
      "start", help="Start the train job")
  jobs_start_parser.add_argument(
      "job_name", help="The name of the job")
  jobs_start_parser.set_defaults(func=util.start_job)

  # subcommand: models
  models_parser = main_subparser.add_parser(
      "models", help="Commands about models")
  models_subparser = models_parser.add_subparsers(
      dest="models_command", help="Subcommands of models")

  # subcommand of models: list
  models_list_parser = models_subparser.add_parser(
      "list", help="List model services")
  models_list_parser.set_defaults(func=util.list_models)

  # subcommand of models: create
  models_create_parser = models_subparser.add_parser(
      "create", help="Create model service")
  models_create_parser.add_argument(
      "-n",
      "--model_name",
      dest="model_name",
      help="The name of the model",
      required=True)
  models_create_parser.add_argument(
      "-v",
      "--model_version",
      dest="model_version",
      help="The version of the model",
      required=True)
  models_create_parser.add_argument(
      "-u",
      "--model_uri",
      dest="model_uri",
      help="The uri of the model",
      required=True)
  models_create_parser.add_argument(
      "-a", "--model_args", dest="model_args", help="The string of args")
  models_create_parser.add_argument(
      "-fe", "--fds_endpoint", dest="fds_endpoint", help="The fds endpoint use")
  models_create_parser.add_argument(
      "-fb", "--fds_bucket", dest="fds_bucket", help="The fds bucket to mount to /fds")
  models_create_parser.add_argument(
      "-c",
      "--cpu_limit",
      dest="cpu_limit",
      help="The CPU limit with unit core")
  models_create_parser.add_argument(
      "-M",
      "--memory_limit",
      dest="memory_limit",
      help="The memory limit with unit M or G")
  models_create_parser.add_argument(
      "-g", "--gpu_limit", dest="gpu_limit", help="The number of GPU limit")
  gpu_type_help = "select gpu type from ({})".format("/".join(constant.GPULIST))
  if not constant.ENABLE_GPU_TYPE_SELECT:
    gpu_type_help = "[DEPRECATED] " + gpu_type_help
  models_create_parser.add_argument(
      "-gt",
      "--gpu_type",
      dest="gpu_type",
      help=gpu_type_help
  )
  models_create_parser.add_argument(
      "-R",
      "--enable_rank",
      dest="enable_rank",
      action="store_true",
      help="Create priority high models"
  )
  models_create_parser.add_argument(
      "-d", "--docker_image", dest="docker_image", help="The docker image")
  models_create_parser.add_argument(
      "--debug",
      dest="debug",
      action="store_true",
      help="debug with tensorflow Serving",
  )
  models_create_parser.add_argument(
      "-dc",
      "--docker_command",
      dest="docker_command",
      help="The docker command")
  models_create_parser.add_argument(
      "-F",
      "--framework",
      dest="framework",
      help="The framework of machine learning")
  models_create_parser.add_argument(
      "-V",
      "--framework_version",
      dest="framework_version",
      help="The version of the framework")
  models_create_parser.add_argument(
      "-r", "--replicas", dest="replicas", help="The num of replicas")
  models_create_parser.add_argument(
      "-pc",
      "--prepare_command",
      dest="prepare_command",
      help="The prepare command")
  models_create_parser.add_argument(
      "-fc",
      "--finish_command",
      dest="finish_command",
      help="The finish command")
  models_create_parser.add_argument(
      "-nsk",
      "--node_selector_key",
      dest="node_selector_key",
      help="The node selector key")
  models_create_parser.add_argument(
      "-nsv",
      "--node_selector_value",
      dest="node_selector_value",
      help="The node selector value")
  models_create_parser.add_argument(
      "-W", "--watch", action="store_true", help="Watch the status of model creation")
  models_create_parser.add_argument(
      "-sv",
      "--save_mode",
      dest="save_mode",
      help="Save model, don't run",
      action = 'store_true'
      )
  models_create_parser.add_argument(
      "--use_seldon",
      dest="use_seldon",
      help="Using seldon service",
      action="store_true"
  )
  models_create_parser.add_argument(
      "--engine_cpu",
      dest="engine_cpu",
      help="The CPU limit with unit core"
  )
  models_create_parser.add_argument(
      "--engine_memory",
      dest="engine_mem",
      help="The memory limit with unit M or G"
  )
  models_create_parser.add_argument(
      "--run_class_name",
      dest="run_class_name",
      help="Load model class name"
  )
  models_create_parser.add_argument(
      "--service_schema",
      dest="service_schema",
      help="Service schema (REST or GRPC)",
      default="GRPC"
  )
  models_create_parser.add_argument(
      "--initial_delay_sec",
      dest="initial_delay_sec",
      help="Initial Delay Seconds"
  )
  models_create_parser.add_argument(
      "--pod_replicas",
      dest="pod_replicas",
      help="The num of pod replicas"
  )
  models_create_parser.add_argument(
      "--use_http",
      dest="use_http",
      action="store_true",
      help="use tensorflow serving restful api"
  )
  models_create_parser.set_defaults(func=util.create_model)

  # subcommand of models: describe
  models_describe_parser = models_subparser.add_parser(
      "describe", help="Describe the model service")
  models_describe_parser.add_argument(
      "model_name", help="The name of the model")
  models_describe_parser.add_argument(
      "model_version", help="The version of the model")
  models_describe_parser.set_defaults(func=util.describe_model)

  # subcommand of models: start
  models_start_parser = models_subparser.add_parser(
      "start", help="Start the model service")
  models_start_parser.add_argument(
      "model_name", help="The name of the model")
  models_start_parser.add_argument(
    "model_version", help="The version of the model")
  models_start_parser.set_defaults(func=util.start_model)

  # subcommand of models: update
  models_update_parser = models_subparser.add_parser(
      "update", help="Update the model service")
  models_update_parser.add_argument(
      "model_name", help="The name of the model")
  models_update_parser.add_argument(
      "-v",
      "--model_version",
      dest="model_version",
      help="The version of the model"
  )
  models_update_parser.add_argument(
      "-u",
      "--model_uri",
      dest="model_uri",
      help="The uri of the model"
  )
  models_update_parser.add_argument(
      "-r",
      "--replicas",
      dest="replicas",
      help="The num of replicas")
  models_update_parser.add_argument(
      "-c",
      "--cpu_limit",
      dest="cpu_limit",
      help="The CPU limit with unit core")
  models_update_parser.add_argument(
      "-M",
      "--memory_limit",
      dest="memory_limit",
      help="The memory limit with unit M or G")
  models_update_parser.add_argument(
      "-g",
      "--gpu_limit",
      dest="gpu_limit",
      help="The number of GPU limit")
  models_update_parser.add_argument(
      "-F",
      "--framework",
      dest="framework",
      help="The framework of machine learning")
  models_update_parser.add_argument(
      "-p",
      "--port",
      dest="port",
      help="Reset Model service port"
  )
  models_update_parser.add_argument(
      "--engine_cpu",
      dest="engine_cpu",
      help="The CPU limit with unit core"
  )
  models_update_parser.add_argument(
      "--engine_memory",
      dest="engine_mem",
      help="The memory limit with unit M or G"
  )
  models_update_parser.set_defaults(func=util.update_model)

  # subcommand of models: logs
  models_logs_parser = models_subparser.add_parser(
      "logs", help="Get the logs of the model service")
  models_logs_parser.add_argument(
      "model_name", help="The name of the model")
  models_logs_parser.add_argument(
      "model_version", help="The version of the model")
  models_logs_parser.add_argument(
      "-ri",
      "--replica_index",
      dest="replica_index",
      help="The replica index"
  )
  models_logs_parser.add_argument(
      "-p",
      "--proxy",
      dest="proxy_logs",
      action="store_true",
      help="Get the logs of the proxy"
  )
  models_logs_parser.set_defaults(func=util.get_model_logs)

  # subcommand of models: metrics
  models_metrics_parser = models_subparser.add_parser(
      "metrics", help="Get the metrics of the model service")
  models_metrics_parser.add_argument("model_name", help="The name of the model")
  models_metrics_parser.add_argument(
      "model_version", help="The version of the model")
  models_metrics_parser.set_defaults(func=util.get_model_metrics)

  # subcommand of models: delete
  models_delete_parser = models_subparser.add_parser(
      "delete", help="Delete the model service")
  models_delete_parser.add_argument("model_name", help="The name of the model")
  models_delete_parser.add_argument(
      "model_version", help="The version of the model")
  models_delete_parser.set_defaults(func=util.delete_model)

  # subcommand of models: predict
  models_predict_parser = models_subparser.add_parser(
      "predict", help="Request the model service and predict")
  models_predict_parser.add_argument(
      "-n",
      "--model_name",
      dest="model_name",
      help="The name of the model",
      required=True)
  models_predict_parser.add_argument(
      "-v",
      "--model_version",
      dest="model_version",
      help="The version of the model")
  models_predict_parser.add_argument(
      "-s", "--server", dest="server", help="The address of the server")
  models_predict_parser.add_argument(
      "-f",
      "--filename",
      dest="filename",
      help="The json data file",
      required=True)
  models_predict_parser.add_argument(
      "-t", "--timeout", dest="timeout", help="The timeout of gRPC request")
  models_predict_parser.set_defaults(func=util.do_predict)

  # subcommand of models: events
  models_events_parser = models_subparser.add_parser(
      "events", help="Get the events of the model service")
  models_events_parser.add_argument(
      "model_name", help="The name of the model service")
  models_events_parser.add_argument(
      "model_version", help="The version of the model service")
  models_events_parser.set_defaults(func=util.get_model_service_events)

  # subcommand: tensorboard
  tensorboard_parser = main_subparser.add_parser(
      "tensorboard", help="Commands about tensorboard")
  tensorboard_subparser = tensorboard_parser.add_subparsers(
      dest="tensorboard_command", help="Subcommands of tensorboard")

  # subcommand of tensorboard: list
  tensorboard_list_parser = tensorboard_subparser.add_parser(
      "list", help="List tensorboards")
  tensorboard_list_parser.set_defaults(func=util.list_tensorboard_services)

  # subcommand of tensorboard: create
  tensorboard_create_parser = tensorboard_subparser.add_parser(
      "create", help="Create tensorboard")
  tensorboard_create_parser.add_argument(
      "-n",
      "--tensorboard_name",
      dest="tensorboard_name",
      help="The name of the tensorboard",
      required=True)
  tensorboard_create_parser.add_argument(
      "-l",
      "--logdir",
      dest="logdir",
      help="The directory of tensorboard log",
      required=True)
  tensorboard_create_parser.add_argument(
      "-R",
      "--enable_rank",
      dest="enable_rank",
      action="store_true",
      help="Create priority high tensorboard"
  )
  tensorboard_create_parser.add_argument(
      "-d", "--docker_image", dest="docker_image", help="The docker image")
  tensorboard_create_parser.add_argument(
      "-dc",
      "--docker_command",
      dest="docker_command",
      help="The docker command")
  tensorboard_create_parser.add_argument(
      "-F",
      "--framework",
      dest="framework",
      help="The framework of machine learning")
  tensorboard_create_parser.add_argument(
      "-V",
      "--framework_version",
      dest="framework_version",
      help="The version of the framework")

  tensorboard_create_parser.add_argument(
      "-fe", "--fds_endpoint",dest="fds_endpoint", help="The fds endpoint use")
  tensorboard_create_parser.add_argument(
      "-fb", "--fds_bucket", dest="fds_bucket", help="The fds bucket to mount to /fds")

  tensorboard_create_parser.add_argument(
      "-nsk",
      "--node_selector_key",
      dest="node_selector_key",
      help="The node selector key")
  tensorboard_create_parser.add_argument(
      "-nsv",
      "--node_selector_value",
      dest="node_selector_value",
      help="The node selector value")

  tensorboard_create_parser.set_defaults(func=util.create_tensorboard_service)

  # subcommand of tensorboard: describe
  tensorboard_describe_parser = tensorboard_subparser.add_parser(
      "describe", help="Describe the tensorboard")
  tensorboard_describe_parser.add_argument(
      "tensorboard_name", help="The name of the tensorboard")
  tensorboard_describe_parser.set_defaults(
      func=util.describe_tensorboard_service)

  # subcommand of tensorboard: delete
  tensorboard_delete_parser = tensorboard_subparser.add_parser(
      "delete", help="Delete the tensorboard(s)")
  tensorboard_delete_parser.add_argument(
      "tensorboard_names", metavar="tensorboard_name", nargs="+", help="The name of the tensorboard")
  tensorboard_delete_parser.set_defaults(func=util.delete_tensorboard_service)

  # subcommand of tensorboard: events
  tensorboard_events_parser = tensorboard_subparser.add_parser(
      "events", help="Get the events of the tensorboard service")
  tensorboard_events_parser.add_argument(
      "tensorboard_name", help="The name of the tensorboard service")
  tensorboard_events_parser.set_defaults(
      func=util.get_tensorboard_service_events)

  # subcommand: dev
  dev_parser = main_subparser.add_parser("dev", help="Commands about dev")
  dev_subparser = dev_parser.add_subparsers(
      dest="dev_command", help="Subcommands of dev")

  # subcommand of dev: list
  dev_list_parser = dev_subparser.add_parser(
      "list", help="List dev environments")
  dev_list_parser.set_defaults(func=util.list_dev_envs)

  # subcommand of dev: create
  dev_create_parser = dev_subparser.add_parser(
      "create", help="Create dev environment")
  dev_create_parser.add_argument(
      "-n",
      "--dev_name",
      dest="dev_name",
      help="The dev environment name",
      required=True)
  dev_create_parser.add_argument(
      "-p",
      "--password",
      dest="password",
      help="The password of ipython notebook",
      required=True)
  dev_create_parser.add_argument(
      "-fe", "--fds_endpoint",dest="fds_endpoint", help="The fds endpoint use")
  dev_create_parser.add_argument(
      "-fb", "--fds_bucket", dest="fds_bucket", help="The fds bucket to mount to /fds")
  #for hdfs
  dev_create_parser.add_argument(
      "-hka", "--hdfs_krb_account", type=str,dest="hdfs_krb_account", help="The kerberos account"
  )
  dev_create_parser.add_argument(
      "-hkp", "--hdfs_krb_password", type=str,dest="hdfs_krb_password", help="The kerberos password"
  )
  dev_create_parser.add_argument(
      "-hkt", "--hdfs_krb_keytab", type=str, dest="hdfs_krb_keytab", help="The kerberos keytab secret name"
  )
  dev_create_parser.add_argument(
      "-he", "--hdfs_endpoint", type=str,dest="hdfs_endpoint", help="The hadoop path to mount to /hdfs"
  )
  dev_create_parser.add_argument(
      "-cv", "--ceph_volume", type=str,dest="ceph_volume", help="The ceph volume name"
  )
  dev_create_parser.add_argument(
      "-cm", "--ceph_mode", type=str,dest="ceph_mode", help="Ceph access mode, r for ReadOnlyMany, rw for ReadWriteOnce"
  )
  dev_create_parser.add_argument(
      "-c",
      "--cpu_limit",
      dest="cpu_limit",
      help="The CPU limit with unit core")
  dev_create_parser.add_argument(
      "-M",
      "--memory_limit",
      dest="memory_limit",
      help="The memory limit with unit K, M or G")
  dev_create_parser.add_argument(
      "-g", "--gpu_limit", dest="gpu_limit", help="The number of GPU limit")
  gpu_type_help = "select gpu type from ({})".format("/".join(constant.GPULIST))
  if not constant.ENABLE_GPU_TYPE_SELECT:
    gpu_type_help = "[DEPRECATED] " + gpu_type_help
  dev_create_parser.add_argument(
      "-gt",
      "--gpu_type",
      dest="gpu_type",
      help=gpu_type_help
  )
  dev_create_parser.add_argument(
      "-R",
      "--enable_rank",
      dest="enable_rank",
      action="store_true",
      help="Create priority high dev"
  )
  dev_create_parser.add_argument(
      "-d", "--docker_image", dest="docker_image", help="The ")
  dev_create_parser.add_argument(
      "-dc",
      "--docker_command",
      dest="docker_command",
      help="The docker command")
  dev_create_parser.add_argument(
      "-F",
      "--framework",
      dest="framework",
      help="The framework of machine learning")
  dev_create_parser.add_argument(
      "-V",
      "--framework_version",
      dest="framework_version",
      help="The version of the framework")
  dev_create_parser.add_argument(
      "-nsk",
      "--node_selector_key",
      dest="node_selector_key",
      help="The node selector key")
  dev_create_parser.add_argument(
      "-nsv",
      "--node_selector_value",
      dest="node_selector_value",
      help="The node selector value")
  dev_create_parser.add_argument(
    "-W", "--watch", action="store_true", help="Watch the status of dev_env creation")
  dev_create_parser.add_argument(
    "-net", "--network", action="store_true", help="network configuration")
  dev_create_parser.set_defaults(func=util.create_dev_env)

  # subcommand of dev: describe
  dev_describe_parser = dev_subparser.add_parser(
      "describe", help="Describe the dev environment")
  dev_describe_parser.add_argument(
      "dev_name", help="The name of dev environment")
  dev_describe_parser.set_defaults(func=util.describe_dev_env)

  # subcommand of dev: stop
  dev_stop_parser = dev_subparser.add_parser(
      "stop", help="Stop the dev environment(s)")
  dev_stop_parser.add_argument(
      "dev_names", metavar="dev_name", nargs="+", help="The name of dev environment")
  dev_stop_parser.set_defaults(func=util.stop_dev_env)

  # subcommand of dev: save
  dev_save_parser = dev_subparser.add_parser(
      "save", help="Save the dev environment(s)")
  dev_save_parser.add_argument(
      "dev_names", metavar="dev_name", nargs="+", help="The name of dev environment")
  dev_save_parser.set_defaults(func=util.save_dev_env)

  # subcommand of dev: restart
  dev_restart_parser = dev_subparser.add_parser(
      "restart", help="Restart the dev environment(s)")
  dev_restart_parser.add_argument(
      "dev_names", metavar="dev_name", nargs="+", help="The name of dev environment")
  dev_restart_parser.set_defaults(func=util.restart_dev_env)

  # subcommand of dev: delete
  dev_delete_parser = dev_subparser.add_parser(
      "delete", help="Delete the dev environment(s)")
  dev_delete_parser.add_argument(
      "dev_names", metavar="dev_name", nargs="+", help="The name of dev environment")
  dev_delete_parser.set_defaults(func=util.delete_dev_env)

  # subcommand of dev: events
  dev_events_parser = dev_subparser.add_parser(
      "events", help="Get the events of the dev environment")
  dev_events_parser.add_argument(
      "dev_name", help="The name of dev environment")
  dev_events_parser.set_defaults(func=util.get_dev_env_events)

  # subcommand of dev: metrics
  dev_metrics_parser = dev_subparser.add_parser(
      "metrics", help="Get the metrics of the dev environment")
  dev_metrics_parser.add_argument(
      "dev_name", help="The name of dev environment")
  dev_metrics_parser.set_defaults(func=util.get_dev_env_metrics)

  # subcommand: dev_server
  dev_server_parser = main_subparser.add_parser(
      "dev_server", help="Commands about dev_server")
  dev_server_subparser = dev_server_parser.add_subparsers(
      dest="dev_server_command", help="Subcommands of dev_server")

  # subcommand of dev_server: list
  dev_server_list_parser = dev_server_subparser.add_parser(
      "list", help="List dev servers")
  dev_server_list_parser.set_defaults(func=util.list_dev_servers)

  # subcommand of dev_server: create
  dev_server_create_parser = dev_server_subparser.add_parser(
      "create", help="Create dev server")
  dev_server_create_parser.add_argument(
      "-n",
      "--dev_name",
      dest="dev_name",
      help="The dev environment name",
      required=True)
  dev_server_create_parser.add_argument(
      "-p",
      "--password",
      dest="password",
      help="The password of ipython notebook",
      required=True)
  dev_server_create_parser.add_argument(
      "-d", "--docker_image", dest="docker_image", help="The ")
  dev_server_create_parser.add_argument(
      "-dc",
      "--docker_command",
      dest="docker_command",
      help="The docker command")
  dev_server_create_parser.add_argument(
      "-F",
      "--framework",
      dest="framework",
      help="The framework of machine learning")
  dev_server_create_parser.add_argument(
      "-V",
      "--framework_version",
      dest="framework_version",
      help="The version of the framework")
  dev_server_create_parser.add_argument(
      "-R",
      "--enable_rank",
      dest="enable_rank",
      action="store_true",
      help="Create priority high dev_server"
  )
  dev_server_create_parser.set_defaults(func=util.create_dev_server)

  # subcommand of dev_server: describe
  dev_server_describe_parser = dev_server_subparser.add_parser(
      "describe", help="Describe the dev server")
  dev_server_describe_parser.add_argument(
      "dev_name", help="The name of dev server")
  dev_server_describe_parser.set_defaults(func=util.describe_dev_server)

  # subcommand of dev_server: delete
  dev_server_delete_parser = dev_server_subparser.add_parser(
      "delete", help="Delete the dev server(s)")
  dev_server_delete_parser.add_argument(
      "dev_names", metavar="dev_name", nargs="+", help="The name of dev server")
  dev_server_delete_parser.set_defaults(func=util.delete_dev_server)

  # subcommand of dev_server: events
  dev_server_events_parser = dev_server_subparser.add_parser(
      "events", help="Get the events of the dev server")
  dev_server_events_parser.add_argument(
      "dev_name", help="The name of dev server")
  dev_server_events_parser.set_defaults(func=util.get_dev_server_events)

  # subcommand: quota
  quota_parser = main_subparser.add_parser(
      "quota", help="Commands about quota")
  quota_subparser = quota_parser.add_subparsers(
      dest="quota_command", help="Subcommands of quota")

  # subcommand of quota: list
  quota_list_parser = quota_subparser.add_parser("list", help="List the quota")
  quota_list_parser.set_defaults(func=util.list_quota)

  # subcommand of quota: list
  quota_update_parser = quota_subparser.add_parser("update", help="Apply for a quota update")
  quota_update_parser.add_argument(
      "-t", 
      "--type", 
      dest="type", 
      help="select service type (dev/jobs/models)",
      required=True
  )
  quota_update_parser.add_argument(
      "-c",
      "--cpu_limit",
      dest="cpu_limit",
      help="The number of CPU limit",
      required=True)
  quota_update_parser.add_argument(
      "-M",
      "--memory_limit",
      dest="memory_limit",
      help="The memory limit, e.g. 2G",
      required=True)
  quota_update_parser.add_argument(
      "-g", 
      "--gpu_limit", 
      dest="gpu_limit", 
      help="The number of GPU limit",
      required=True)
  quota_update_parser.set_defaults(func=util.apply_quota)
  
  # subcommand: framework
  framework_parser = main_subparser.add_parser(
      "framework", help="Commands about framework")
  framework_subparser = framework_parser.add_subparsers(
      dest="framework_command", help="Subcommands of framework")

  # subcommand of framework: list
  framework_list_parser = framework_subparser.add_parser(
      "list", help="List the frameworks")
  framework_list_parser.set_defaults(func=util.list_framework)


  # subcommand of pipeline
  pipeline_parser = main_subparser.add_parser(
    "pipeline", help="Commands about pipeline")
  pipeline_subparser = pipeline_parser.add_subparsers(
    dest="pipeline_command", help="Subcommands of pipeline")

  # subcommand of pipeline: list
  pipeline_list_parser = pipeline_subparser.add_parser(
    "list", help="List pipelines")
  pipeline_list_parser.set_defaults(func=util.list_pipelines)

  # subcommand of pipeline: list
  pipeline_schedule_parser = pipeline_subparser.add_parser(
    "schedulelist", help="Pipeline schedule")
  pipeline_schedule_parser.add_argument("pipeline_name", help="The pipeline name of the schedule")
  pipeline_schedule_parser.set_defaults(func=util.list_pipeline_schedules)


  # subcommand of pipeline: list
  pipeline_schedule_parser = pipeline_subparser.add_parser(
    "scheduledescribe", help="Describe Pipeline schedule")
  pipeline_schedule_parser.add_argument("schedule_id", help="The id of the schedule")
  pipeline_schedule_parser.set_defaults(func=util.describe_pipeline_schedule)

  # subcommand of pipeline: list
  pipeline_schedule_parser = pipeline_subparser.add_parser(
    "schedule", help="Pipeline schedule")
  pipeline_schedule_parser.add_argument("pipeline_name", help="The pipeline name of the schedule")
  pipeline_schedule_parser.add_argument("-d", "--pipeline_rerun_date", help="The expected run date of the schedule")
  pipeline_schedule_parser.set_defaults(func=util.create_pipeline_schedule)


  # subcommand of pipeline: delete
  pipeline_delete_parser = pipeline_subparser.add_parser(
      "delete", help="Delete the pipeline(s)")
  pipeline_delete_parser.add_argument("pipeline_names",
                                      metavar="pipeline_name",
                                      nargs="+",
                                      help="The name of the pipeline")
  pipeline_delete_parser.set_defaults(func=util.delete_pipeline)

  # subcommand of pipeline: describe
  pipeline_describe_parser = pipeline_subparser.add_parser(
    "describe", help="Describe pipeline")
  pipeline_describe_parser.add_argument("pipeline_name", help="The pipeline to describe")
  pipeline_describe_parser.set_defaults(func=util.describe_pipeline)

  # subcommand of pipeline: logs
  pipeline_logs_parser = pipeline_subparser.add_parser(
      "logs", help="Get the logs of the pipeline pod")
  pipeline_logs_parser.add_argument("pod_name", help="The pod name of the pipeline")
  pipeline_logs_parser.set_defaults(func=util.get_pipeline_logs)

  # subcommand of pipeline: logs
  pipeline_schedule_logs_parser = pipeline_subparser.add_parser(
      "schedulelogs", help="Get the logs of the pipeline schedule pod")
  pipeline_schedule_logs_parser.add_argument("pod_name", help="The pod name of the pipeline")
  pipeline_schedule_logs_parser.set_defaults(func=util.get_pipeline_logs)

  # subcommand of pipeline: start
  pipeline_start_parser = pipeline_subparser.add_parser(
      "start", help="start the pipeline")
  pipeline_start_parser.add_argument("pipeline_name", help="The name of the pipeline")
  pipeline_start_parser.set_defaults(func=util.start_pipeline)

  # subcommand of pipeline: stop
  pipeline_stop_parser = pipeline_subparser.add_parser(
      "stop", help="Stop the pipeline")
  pipeline_stop_parser.add_argument("pipeline_name", help="The name of the pipeline")
  pipeline_stop_parser.set_defaults(func=util.stop_pipeline)

  # subcommand of pipeline: stop
  pipeline_rerun_parser = pipeline_subparser.add_parser(
      "rerun", help="Rerun the pipeline")
  pipeline_rerun_parser.add_argument("pipeline_name", help="The name of the pipeline")
  pipeline_rerun_parser.add_argument(
    "-sn", "--start_node", dest="start_node", help="The start_node")
  pipeline_rerun_parser.add_argument(
    "-dr", "--date_range", dest="date_range", help="The date_range")
  pipeline_rerun_parser.set_defaults(func=util.rerun_pipeline)


  # subcommand of pipeline : create
  pipeline_create_parser = pipeline_subparser.add_parser(
    "create", help="Create pipeline")
  pipeline_create_parser.add_argument(
    "-n", "--pipeline_name", dest="pipeline_name", help="The pipeline name")
  pipeline_update_parser = pipeline_subparser.add_parser(
    "update", help="Update pipeline")
  pipeline_update_parser.add_argument("pipeline_name", help="The name of the pipeline")

  def add_pipeline_create_update_argument():
    for parser in [pipeline_update_parser, pipeline_create_parser]:
      parser.add_argument(
        "-f",
        "--filename",
        dest="filename",
        help="The json file contains the pipeline task msg")
      parser.add_argument(
        "-a", "--pipeline_config", dest="pipeline_config", help="The string of config ")
      parser.add_argument(
        "-fe", "--fds_endpoint", dest="fds_endpoint", help="The fds endpoint use")
      parser.add_argument(
        "-fb", "--fds_bucket", dest="fds_bucket", help="The fds bucket to mount to /fds")
      # for hdfs
      parser.add_argument(
        "-hka", "--hdfs_krb_account", type=str, dest="hdfs_krb_account", help="The kerberos account"
      )
      parser.add_argument(
        "-hkp", "--hdfs_krb_password", type=str, dest="hdfs_krb_password", help="The kerberos password"
      )
      parser.add_argument(
        "-hkt", "--hdfs_krb_keytab", type=str, dest="hdfs_krb_keytab", help="The kerberos keytab secret name"
      )
      parser.add_argument(
        "-he", "--hdfs_endpoint", type=str, dest="hdfs_endpoint", help="The hadoop path to mount to /hdfs"
      )
      parser.add_argument(
        "-ce", "--cloudml_endpoint", type=str, dest="cloudml_endpoint", help="The cloudml endpoint")
      parser.add_argument(
        "-om", "--org_mail", type=str, dest="org_mail", help="The org mail")
      parser.add_argument(
          "-sv",
          "--save_mode",
          dest="save_mode",
          help="Save pipeline, don't run",
          action='store_true')
      parser.add_argument(
          "-W", "--watch", action="store_true", help="Watch the status of pipeline")
  add_pipeline_create_update_argument()
  pipeline_create_parser.set_defaults(func=util.create_pipeline)
  pipeline_update_parser.set_defaults(func=util.update_pipeline)


  # subcommand: ceph
  ceph_parser = main_subparser.add_parser(
      "ceph", help="Commands about ceph volume")
  ceph_subparser = ceph_parser.add_subparsers(
      dest="ceph_command", help="Subcommands of ceph")

  # subcommand of ceph: list
  ceph_list_parser = ceph_subparser.add_parser(
      "list", help="List ceph volumes")
  ceph_list_parser.set_defaults(func=util.list_cephs)

  # subcommand of ceph: create
  ceph_create_parser = ceph_subparser.add_parser(
      "create", help="Create a ceph volume")
  ceph_create_parser.add_argument(
      "-n",
      "--ceph_name",
      dest="ceph_name",
      help="The name of ceph volume",
      required=True)
  ceph_create_parser.add_argument(
      "-c",
      "--capacity",
      dest="capacity",
      help="The capacity of ceph volume, e.g. 2M, 3G, 4T",
      required=True)
  ceph_create_parser.set_defaults(func=util.create_ceph)

  # subcommand of ceph: describe
  ceph_describe_parser = ceph_subparser.add_parser(
      "describe", help="Describe a ceph volume")
  ceph_describe_parser.add_argument(
      "ceph_name", help="The name of the ceph volume")
  ceph_describe_parser.set_defaults(
      func=util.describe_ceph)

  # subcommand of ceph: delete
  ceph_delete_parser = ceph_subparser.add_parser(
      "delete", help="Delete ceph volume(s)")
  ceph_delete_parser.add_argument(
      "ceph_names", metavar="ceph_name", nargs="+", help="The name of the ceph volume")
  ceph_delete_parser.add_argument(
      "-f", "--force", action="store_true", help="ignore ceph status and mount")
  ceph_delete_parser.set_defaults(func=util.delete_ceph)

  # subcommand of ceph: events
  ceph_events_parser = ceph_subparser.add_parser(
      "events", help="Get the events of the ceph volume")
  ceph_events_parser.add_argument(
      "ceph_name", help="The name of the ceph volume")
  ceph_events_parser.set_defaults(
      func=util.get_ceph_events)


  # subcommand: secret
  secret_parser = main_subparser.add_parser(
      "secret", help="Commands about secret")
  secret_subparser = secret_parser.add_subparsers(
      dest="secret_command", help="Subcommands of secret")

  # subcommand of secret: list
  secret_list_parser = secret_subparser.add_parser(
      "list", help="List secrets")
  secret_list_parser.set_defaults(func=util.list_secret_services)

  # subcommand of secret: create
  secret_create_parser = secret_subparser.add_parser(
      "create", help="Create secret")
  secret_create_parser.add_argument(
      "-n",
      "--secret_name",
      dest="secret_name",
      help="The name of the secret",
      required=True)
  secret_create_parser.add_argument(
      "-f",
      "--file_path",
      dest="file_path",
      help="The file path that used to create secret with.",
      required=True)
  secret_create_parser.set_defaults(func=util.create_secret_service)

  # subcommand of secret: describe
  secret_describe_parser = secret_subparser.add_parser(
      "describe", help="Describe the secret")
  secret_describe_parser.add_argument(
      "secret_name", help="The name of the secret")
  secret_describe_parser.set_defaults(
      func=util.describe_secret_service)

  # subcommand of secret: delete
  secret_delete_parser = secret_subparser.add_parser(
      "delete", help="Delete the secret(s)")
  secret_delete_parser.add_argument(
      "secret_names", metavar="secret_name", nargs="+", help="The name of the secret")
  secret_delete_parser.set_defaults(func=util.delete_secret_service)

  # subcommand of schedule
  schedule_parser = main_subparser.add_parser(
    "schedule", help="Commands about schedule")
  schedule_subparser = schedule_parser.add_subparsers(
    dest="schedule_command", help="Subcommands of schedule")

  # subcommand of schedule: list
  schedule_list_parser = schedule_subparser.add_parser(
    "list", help="List schedules")
  schedule_list_parser.set_defaults(func=util.list_schedules)

  # subcommand of schedule: delete
  schedule_delete_parser = schedule_subparser.add_parser(
    "delete", help="Delete the schedule(s)")
  schedule_delete_parser.add_argument("schedule_names",
                                      metavar="schedule_name",
                                      nargs="+",
                                      help="The name of the schedule")
  schedule_delete_parser.set_defaults(func=util.delete_schedule)

  # subcommand of schedule: describe
  schedule_describe_parser = schedule_subparser.add_parser(
    "describe", help="Describe schedule")
  schedule_describe_parser.add_argument("schedule_name", help="The schedule to describe")
  schedule_describe_parser.set_defaults(func=util.describe_schedule)

  # subcommand of schedule: start
  schedule_start_parser = schedule_subparser.add_parser(
    "start", help="start the schedule")
  schedule_start_parser.add_argument("schedule_name", help="The name of the schedule")
  schedule_start_parser.set_defaults(func=util.start_schedule)

  # subcommand of schedule: stop
  schedule_stop_parser = schedule_subparser.add_parser(
    "stop", help="Stop the schedule")
  schedule_stop_parser.add_argument("schedule_name", help="The name of the schedule")
  schedule_stop_parser.set_defaults(func=util.stop_schedule)

  # subcommand of schedule : create
  schedule_create_parser = schedule_subparser.add_parser(
    "create", help="Create schedule")
  schedule_create_parser.add_argument(
    "-n", "--schedule_name", dest="schedule_name", help="The schedule name")
  schedule_update_parser = schedule_subparser.add_parser(
    "update", help="Update schedule")
  schedule_update_parser.add_argument("schedule_name", help="The name of the schedule")

  def add_schedule_create_update_argument():
    for parser in [schedule_update_parser, schedule_create_parser]:
      parser.add_argument(
        "-rn",
        "--resource_name",
        type=str,
        dest="resource_name",
        help="The resource_name of the schedule")
      parser.add_argument(
        "-rt", "--resource_type", type=str, dest="resource_type", help="The type of the schedule resource")
      parser.add_argument(
        "-p", "--cron_param", type=str, dest="cron_param", help="The cron param of the schedule")
      parser.add_argument(
        "-shl", "--success_history_limit", dest="success_history_limit", type=int, help="The success history limit of the schedule")
      # for hdfs
      parser.add_argument(
        "-fhl", "--failed_history_limit", type=int, dest="failed_history_limit", help="The failed history limit of the schedule"
      )
      parser.add_argument(
        "-spd", "--suspend", type=str2bool, dest="suspend", help="Whether to suspend the schedule when create"
      )
      parser.add_argument(
        "-cp", "--concurrency_policy", type=str, dest="concurrency_policy", help="The concurrent policy of the schedule: Allow Replace Forbid"
      )
      parser.add_argument(
        "-d", "--image_name", type=str, dest="image_name", help="The image name of the cronjob")

  def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
      return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
      return False
    else:
      raise argparse.ArgumentTypeError('Boolean value( yes, no, true, false ....) expected.')
  add_schedule_create_update_argument()
  schedule_create_parser.set_defaults(func=util.create_schedule)
  schedule_update_parser.set_defaults(func=util.update_schedule)

  # subcommand: all
  all_parser = main_subparser.add_parser(
      "all", help="Commands about all")
  all_subparser = all_parser.add_subparsers(
      dest="all_command", help="Subcommands of all")

  # subcommand of all: list
  all_list_parser = all_subparser.add_parser(
      "list", help="List all resources")
  all_list_parser.set_defaults(func=util.list_all)

  # subcommand: cluster resources info
  resources_parser = main_subparser.add_parser(
      "resources", help="Commands about available resources"
  )
  resources_subparser = resources_parser.add_subparsers(
      dest = "resources_command", help= "Subcommands of resources"
  )
  # subcommand of resources: list
  resources_list_parser = resources_subparser.add_parser(
      "list", help="list cluster available resources"
  )
  resources_list_parser.set_defaults(func=util.list_cluster_available_resources)





  # For auto-complete
  argcomplete.autocomplete(parser)


  if len(sys.argv) == 1:
    args = parser.parse_args(["-h"])
  else:

    args = parser.parse_args(sys.argv[1:])
  args.func(args)


if __name__ == "__main__":
  main()
