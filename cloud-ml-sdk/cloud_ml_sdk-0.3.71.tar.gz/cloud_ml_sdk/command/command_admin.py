#!/usr/bin/env python

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

import argparse
import logging
import sys
sys.path.append("../../")

from . import util

logging.basicConfig(level=logging.DEBUG)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
      "-k", "--context", dest="config_context_name", action=util.SetConfigContextEnv,
      help="The cloudml config context name, available values can be listed by: cloudml config show")

  main_subparser = parser.add_subparsers(dest="command_group", help="Commands")

  # subcommand: hptunings
  hptunings_parser = main_subparser.add_parser("hp", help="Commands about hp jobs")
  hptunings_subparser = hptunings_parser.add_subparsers(
      dest="hp_command", help="Subcommands of hp jobs")

  # subcommand of hptunings: list
  hptunings_list_parser = hptunings_subparser.add_parser("list", help="List hp jobs")
  hptunings_list_parser.add_argument(
      "org_id", help="The org_id to list (with -1 stand for all)")
  hptunings_list_parser.set_defaults(func=util.list_hp)

  # subcommand of jobs: describe
  hptunings_describe_parser = hptunings_subparser.add_parser(
      "describe", help="Describe hp job")
  hptunings_describe_parser.add_argument("hp_name", help="The name of the hp job")
  hptunings_describe_parser.add_argument(
      "org_id", help="The org_id of the hp job's owner")
  hptunings_describe_parser.set_defaults(func=util.describe_hp_job)


  # subcommand of hptunings: get trials
  hptuning_trials_parser = hptunings_subparser.add_parser("trials", help="get trials")
  hptuning_trials_parser.add_argument("hp_name",
                                      help="the hptuning job the trials belong to")
  hptuning_trials_parser.add_argument(
      "org_id", help="The org_id of the hp job's owner")
  hptuning_trials_parser.set_defaults(func=util.get_trials)


  # subcommand of hp jobs: logs
  hptunings_trial_logs_parser = hptunings_subparser.add_parser(
      "logs", help="Get the logs of the hp job trial")
  hptunings_trial_logs_parser.add_argument("hp_name",help="the hptuning job the trials belong to")

  hptunings_trial_logs_parser.add_argument("-ti",
                                         "--trial_id",
                                         dest="trial_id",
                                         help="the log of the trial(pod)")
  hptunings_trial_logs_parser.add_argument("-f", "--follow", action="store_true",
                                help="Follow the log stream of the pod. Defaults to false.")
  hptunings_trial_logs_parser.add_argument("-n", "--lines", type=int, help="The last number of lines to show.")

  hptunings_trial_logs_parser.add_argument(
      "org_id", help="The org_id of the hp job's owner")
  hptunings_trial_logs_parser.set_defaults(func=util.get_trial_log)


  # subcommand of hp jobs: events
  hptunings_events_parser = hptunings_subparser.add_parser(
      "events", help="Get the events of the hp job")
  hptunings_events_parser.add_argument("hp_name", help="The name of the hp job")
  hptunings_events_parser.add_argument(
      "org_id", help="The org_id of the hp job's owner")
  hptunings_events_parser.set_defaults(func=util.get_hp_job_events)

  # subcommand: jobs
  jobs_parser = main_subparser.add_parser("jobs", help="Commands about jobs")
  jobs_subparser = jobs_parser.add_subparsers(
      dest="job_command", help="Subcommands of jobs")

  # subcommand of jobs: list
  jobs_list_parser = jobs_subparser.add_parser("list", help="List jobs")
  jobs_list_parser.add_argument(
      "org_id", help="The org_id to list (with -1 stand for all)")
  jobs_list_parser.set_defaults(func=util.list_jobs)

  # subcommand of jobs: describe
  jobs_describe_parser = jobs_subparser.add_parser(
      "describe", help="Describe job")
  jobs_describe_parser.add_argument("job_name", help="The name of the job")
  jobs_describe_parser.add_argument(
      "org_id", help="The org_id of the job's owner")
  jobs_describe_parser.set_defaults(func=util.describe_job)

  # subcommand of jobs: logs
  jobs_logs_parser = jobs_subparser.add_parser(
      "logs", help="Get the logs of the job")
  jobs_logs_parser.add_argument("-f", "--follow", action="store_true",
                                help="Follow the log stream of the pod. Defaults to false.")
  jobs_logs_parser.add_argument("-n", "--lines", type=int, help="The last number of lines to show.")
  jobs_logs_parser.add_argument("job_name", help="The job to get the logs")
  jobs_logs_parser.add_argument(
      "org_id", help="The org_id of the job's owner")
  jobs_logs_parser.set_defaults(func=util.get_job_logs)

  # subcommand of jobs: events
  jobs_events_parser = jobs_subparser.add_parser(
      "events", help="Get the events of the train job")
  jobs_events_parser.add_argument("job_name", help="The name of the train job")
  jobs_events_parser.add_argument(
      "org_id", help="The org_id of the job's owner")
  jobs_events_parser.set_defaults(func=util.get_train_job_events)

  # subcommand of jobs: delete
  jobs_delete_parser = jobs_subparser.add_parser(
      "delete", help="Delete the job(s)")
  jobs_delete_parser.add_argument("job_names", metavar="job_name", nargs="+", help="The name of the job")
  jobs_delete_parser.add_argument("org_id", help="The org_id of the job's owner")
  jobs_delete_parser.set_defaults(func=util.delete_job)

  # subcommand: model
  models_parser = main_subparser.add_parser(
      "models", help="Commands about models")
  models_subparser = models_parser.add_subparsers(
      dest="model_command", help="Subcommands of models")

  # subcommand of models: list
  models_list_parser = models_subparser.add_parser("list", help="List models")
  models_list_parser.add_argument(
      "org_id", help="The org_id to list (with -1 stand for all)")
  models_list_parser.set_defaults(func=util.list_models)

  # subcommand of models: describe
  models_describe_parser = models_subparser.add_parser(
      "describe", help="Describe model")
  models_describe_parser.add_argument(
      "model_name", help="The name of the model")
  models_describe_parser.add_argument(
      "model_version", help="The version of the model")
  models_describe_parser.add_argument(
      "org_id", help="The org_id of the model's owner")
  models_describe_parser.set_defaults(func=util.describe_model)

  # subcommand of models: logs
  models_logs_parser = models_subparser.add_parser(
      "logs", help="Get the logs of the model service")
  models_logs_parser.add_argument("model_name", help="The name of the model")
  models_logs_parser.add_argument(
      "model_version", help="The version of the model")
  models_logs_parser.add_argument(
      "org_id", help="The org_id of the model's owner")
  models_logs_parser.set_defaults(func=util.get_model_logs)

  # subcommand of models: events
  models_events_parser = models_subparser.add_parser(
      "events", help="Get the events of the model service")
  models_events_parser.add_argument(
      "model_name", help="The name of the model service")
  models_events_parser.add_argument(
      "model_version", help="The version of the model service")
  models_events_parser.add_argument(
      "org_id", help="The org_id of the model's owner")
  models_events_parser.set_defaults(func=util.get_model_service_events)

    # subcommand of models: delete
  models_delete_parser = models_subparser.add_parser(
      "delete", help="Delete the model service")
  models_delete_parser.add_argument("model_name", help="The name of the model")
  models_delete_parser.add_argument(
      "model_version", help="The version of the model")
  models_delete_parser.add_argument(
      "org_id", help="The org_id of the model's owner")
  models_delete_parser.set_defaults(func=util.delete_model)

  # subcommand: dev
  dev_parser = main_subparser.add_parser("dev", help="Commands about dev")
  dev_subparser = dev_parser.add_subparsers(
      dest="dev_command", help="Subcommands of dev")

  # subcommand of dev: list
  dev_list_parser = dev_subparser.add_parser("list", help="List devs")
  dev_list_parser.add_argument(
      "org_id", help="The org_id to list (with -1 stand for all)")
  dev_list_parser.set_defaults(func=util.list_dev_envs)

  # subcommand of dev: describe
  dev_describe_parser = dev_subparser.add_parser(
      "describe", help="Describe dev")
  dev_describe_parser.add_argument("dev_name", help="The name of the dev")
  dev_describe_parser.add_argument(
      "org_id", help="The org_id of the dev's owner")
  dev_describe_parser.set_defaults(func=util.describe_dev_env)

  # subcommand: dev_server
  dev_server_parser = main_subparser.add_parser(
      "dev_server", help="Commands about dev_server")
  dev_server_subparser = dev_server_parser.add_subparsers(
      dest="dev_server_command", help="Subcommands of dev_server")

  # subcommand of dev_server: list
  dev_server_list_parser = dev_server_subparser.add_parser(
      "list", help="List dev_servers")
  dev_server_list_parser.add_argument(
      "org_id", help="The org_id to list (with -1 stand for all)")
  dev_server_list_parser.set_defaults(func=util.list_dev_servers)

  # subcommand of dev_server: describe
  dev_server_describe_parser = dev_server_subparser.add_parser(
      "describe", help="Describe dev_server")
  dev_server_describe_parser.add_argument(
      "dev_name", help="The name of the dev_server")
  dev_server_describe_parser.add_argument(
      "org_id", help="The org_id of the dev_server's owner")
  dev_server_describe_parser.set_defaults(func=util.describe_dev_server)

    # subcommand of dev: stop
  dev_stop_parser = dev_subparser.add_parser(
      "stop", help="Stop the dev environment(s)")
  dev_stop_parser.add_argument(
      "dev_names", metavar="dev_name", nargs="+", help="The name of dev environment")
  dev_stop_parser.add_argument("org_id", help="The org_id of the dev's owner")
  dev_stop_parser.set_defaults(func=util.stop_dev_env)

  # subcommand of dev: save
  dev_save_parser = dev_subparser.add_parser(
      "save", help="Save the dev environment(s)")
  dev_save_parser.add_argument(
      "dev_names", metavar="dev_name", nargs="+", help="The name of dev environment")
  dev_save_parser.add_argument("org_id", help="The org_id of the dev's owner")
  dev_save_parser.set_defaults(func=util.save_dev_env)

  # subcommand of dev: restart
  dev_restart_parser = dev_subparser.add_parser(
      "restart", help="Restart the dev environment(s)")
  dev_restart_parser.add_argument(
      "dev_names", metavar="dev_name", nargs="+", help="The name of dev environment")
  dev_restart_parser.add_argument("org_id", help="The org_id of the dev's owner")
  dev_restart_parser.set_defaults(func=util.restart_dev_env)

  # subcommand of dev: delete
  dev_delete_parser = dev_subparser.add_parser(
      "delete", help="Delete the dev environment(s)")
  dev_delete_parser.add_argument(
      "dev_names", metavar="dev_name", nargs="+", help="The name of dev environment")
  dev_delete_parser.add_argument("org_id", help="The org_id of the dev's owner")
  dev_delete_parser.set_defaults(func=util.delete_dev_env)

  # subcommand: tensorboard
  tensorboard_parser = main_subparser.add_parser(
      "tensorboard", help="Commands about tensorboard")
  tensorboard_subparser = tensorboard_parser.add_subparsers(
      dest="tensorboard_command", help="Subcommands of tensorboard")

  # subcommand of tensorboard: list
  tensorboard_list_parser = tensorboard_subparser.add_parser(
      "list", help="List tensorboard")
  tensorboard_list_parser.add_argument(
      "org_id", help="The org_id to list (with -1 stand for all)")
  tensorboard_list_parser.set_defaults(func=util.list_tensorboard_services)

  # subcommand of tensorboard: describe
  tensorboard_describe_parser = tensorboard_subparser.add_parser(
      "describe", help="Describe tensorboard")
  tensorboard_describe_parser.add_argument(
      "tensorboard_name", help="The name of the tensorboard")
  tensorboard_describe_parser.add_argument(
      "org_id", help="The org_id of the tensorboard's owner")
  tensorboard_describe_parser.set_defaults(
      func=util.describe_tensorboard_service)

    # subcommand of tensorboard: delete
  tensorboard_delete_parser = tensorboard_subparser.add_parser(
      "delete", help="Delete the tensorboard(s)")
  tensorboard_delete_parser.add_argument(
      "tensorboard_names", metavar="tensorboard_name", nargs="+", help="The name of the tensorboard")
  tensorboard_describe_parser.add_argument(
      "org_id", help="The org_id of the tensorboard's owner")
  tensorboard_delete_parser.set_defaults(func=util.delete_tensorboard_service)

  # subcommand: quota
  quota_parser = main_subparser.add_parser(
      "quota", help="Commands about quota")
  quota_subparser = quota_parser.add_subparsers(
      dest="quota_command", help="Subcommands of quota")

  # subcommand of quota: list
  quota_list_parser = quota_subparser.add_parser("list", help="List the quota")
  quota_list_parser.add_argument(
      "org_id", help="Org_id to list (with -1 stand for all)")
  quota_list_parser.set_defaults(func=util.list_quota)

  # subcommand of quota: update
  quota_update_parser = quota_subparser.add_parser(
      "update", help="Update quota")
  quota_update_parser.add_argument("org_id", help="The org_id to set")
  quota_update_parser.add_argument(
      "-n", "--org_name", dest="org_name", help="The org_name to set")
  quota_update_parser.add_argument(
      "-t",
      "--type",
      dest="type",
      help="The job type to update, support for jobs, models, dev, tensorboard, total")
  quota_update_parser.add_argument(
      "-c", "--cpu", dest="cpu", help="The new cpu quota")
  quota_update_parser.add_argument(
      "-m", "--memory", dest="memory", help="The new memory quota")
  quota_update_parser.add_argument(
      "-g", "--gpu", dest="gpu", help="The new gpu quota")
  quota_update_parser.add_argument(
      "-T",
      "--tensorboard",
      dest="tensorboard",
      help="The new tensorboard quota")
  quota_update_parser.add_argument(
      "-C", "--count", dest="count", help="The count quota")
  quota_update_parser.add_argument(
      "-R", "--priority_quota", dest="priority_quota", help="The priority high quota"
  )
  quota_update_parser.add_argument(
      "-P", "--priority",dest="priority", help="Set priority rank"
  )
  quota_update_parser.add_argument(
      "-M", "--org_mail",dest="org_mail", help="Set org mail"
  )
  quota_update_parser.add_argument(
    "-proj", "--project", dest="project", help="the project name"
  )
  quota_update_parser.set_defaults(func=util.update_quota)

  # subcommand: ceph
  ceph_parser = main_subparser.add_parser(
      "ceph", help="Commands about ceph volume")
  ceph_subparser = ceph_parser.add_subparsers(
      dest="ceph_command", help="Subcommands of ceph")

  # subcommand of ceph: list
  ceph_list_parser = ceph_subparser.add_parser(
      "list", help="List ceph volumes")
  ceph_list_parser.add_argument("org_id", help="The org id of ceph volumes (with -1 stand for all)")
  ceph_list_parser.set_defaults(func=util.list_cephs)

  # subcommand of ceph: describe
  ceph_describe_parser = ceph_subparser.add_parser(
      "describe", help="Describe a ceph volume")
  ceph_describe_parser.add_argument(
      "ceph_name", help="The name of the ceph volume")
  ceph_describe_parser.add_argument("org_id", help="The org id of ceph volume (with -1 stand for all)")
  ceph_describe_parser.set_defaults(
      func=util.describe_ceph)

  # subcommand of ceph: delete
  ceph_delete_parser = ceph_subparser.add_parser(
      "delete", help="Delete ceph volume(s)")
  ceph_delete_parser.add_argument(
      "ceph_names", metavar="ceph_name", nargs="+", help="The name of the ceph volume")
  ceph_delete_parser.add_argument(
      "-f", "--force", action="store_true", help="ignore ceph status and mount")
  ceph_delete_parser.add_argument("org_id", help="The org id of ceph volume (with -1 stand for all)")
  ceph_delete_parser.set_defaults(func=util.delete_ceph)

  # subcommand of ceph: events
  ceph_events_parser = ceph_subparser.add_parser(
      "events", help="Get the events of the ceph volume")
  ceph_events_parser.add_argument(
      "ceph_name", help="The name of the ceph volume")
  ceph_events_parser.add_argument("org_id", help="The org id of ceph volume (with -1 stand for all)")
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
  secret_list_parser.add_argument(
      "org_id", help="The org_id of the secret's owner")
  secret_list_parser.set_defaults(func=util.list_secret_services)

  # subcommand of secret: describe
  secret_describe_parser = secret_subparser.add_parser(
      "describe", help="Describe the secret")
  secret_describe_parser.add_argument(
      "secret_name", help="The name of the secret")
  secret_describe_parser.add_argument(
      "org_id", help="The org_id of the secret's owner")
  secret_describe_parser.set_defaults(
      func=util.describe_secret_service)

  # subcommand of secret: delete
  secret_delete_parser = secret_subparser.add_parser(
      "delete", help="Delete the secret(s)")
  secret_delete_parser.add_argument(
      "secret_names", metavar="secret_name", nargs="+", help="The name of the secret")
  secret_delete_parser.add_argument(
      "org_id", help="The org_id of the secret's owner")
  secret_delete_parser.set_defaults(func=util.delete_secret_service)


  # subcommand: namespace
  namespace_parser = main_subparser.add_parser(
      "namespace", help="Commands about namespace")
  namespace_subparser = namespace_parser.add_subparsers(
      dest="namespace_command", help="Subcommands of namespace")

  # subcommand of namespace: list
  namespace_list_parser = namespace_subparser.add_parser(
      "list", help="List namespaces")
  namespace_list_parser.set_defaults(func=util.list_namespaces)

  # subcommand of namespace: describe
  namespace_describe_parser = namespace_subparser.add_parser(
      "describe", help="Describe the namespace")
  namespace_describe_parser.add_argument(
      "name", help="The name of the namespace")
  namespace_describe_parser.set_defaults(
      func=util.describe_namespace)

  # subcommand of namespace: create
  namespace_create_parser = namespace_subparser.add_parser(
      "create", help="Create the namespace")
  namespace_create_parser.add_argument(
      "-n", "--name", required=True, dest="name", help="The name of the namespace")
  namespace_create_parser.add_argument(
      "-e", "--owner_email", dest="owner_email", help="The email of the namespace owner")
  namespace_create_parser.add_argument(
      "-d", "--description", dest="description", help="The description of the namespace")
  namespace_create_parser.set_defaults(
      func=util.create_namespace)

  # subcommand of namespace: update
  namespace_update_parser = namespace_subparser.add_parser(
      "update", help="Update the namespace")
  namespace_update_parser.add_argument(
      "name", help="The name of the namespace to update")
  namespace_update_parser.add_argument(
      "-e", "--owner_email", dest="owner_email", help="The email of the namespace owner")
  namespace_update_parser.add_argument(
      "-d", "--description", dest="description", help="The description of the namespace")
  namespace_update_parser.set_defaults(
      func=util.update_namespace)

  # subcommand of namespace: delete
  namespace_delete_parser = namespace_subparser.add_parser(
      "delete", help="Delete the namespace(s). Warning: This deletes everything under the namespace!")
  namespace_delete_parser.add_argument(
      "names", metavar="name", nargs="+", help="The name of the namespace")
  namespace_delete_parser.set_defaults(func=util.delete_namespace)


  # subcommand: namespace_quota
  namespace_quota_parser = main_subparser.add_parser(
      "namespace_quota", help="Commands about namespace_quota")
  namespace_quota_subparser = namespace_quota_parser.add_subparsers(
      dest="namespace_quota_command", help="Subcommands of namespace_quota")

  # subcommand of namespace_quota: list
  namespace_quota_list_parser = namespace_quota_subparser.add_parser("list", help="List the namespace_quota")
  namespace_quota_list_parser.set_defaults(func=util.list_namespace_quota)

  # subcommand of namespace_quota: create
  namespace_quota_create_parser = namespace_quota_subparser.add_parser(
      "create", help="Create namespace_quota")
  namespace_quota_create_parser.add_argument("name", help="The namespace to set")
  namespace_quota_create_parser.add_argument(
      "-c", "--cpu", dest="cpu", type=int, help="The cpu namespace_quota")
  namespace_quota_create_parser.add_argument(
      "-m", "--memory", dest="memory", type=int, help="The memory namespace_quota, unit Gi")
  namespace_quota_create_parser.add_argument(
      "-g", "--gpu", dest="gpu", type=int, help="The gpu namespace_quota")
  namespace_quota_create_parser.set_defaults(func=util.create_namespace_quota)

  # subcommand of namespace_quota: update
  namespace_quota_update_parser = namespace_quota_subparser.add_parser(
      "update", help="Update namespace_quota")
  namespace_quota_update_parser.add_argument("name", help="The namespace to set")
  namespace_quota_update_parser.add_argument(
      "-c", "--cpu", dest="cpu", type=int, help="The cpu namespace_quota")
  namespace_quota_update_parser.add_argument(
      "-m", "--memory", dest="memory", type=int, help="The memory namespace_quota, unit Gi")
  namespace_quota_update_parser.add_argument(
      "-g", "--gpu", dest="gpu", type=int, help="The gpu namespace_quota")
  namespace_quota_update_parser.set_defaults(func=util.update_namespace_quota)


  # subcommand: namespace_user
  namespace_user_parser = main_subparser.add_parser(
      "namespace_user", help="Commands about namespace_user")
  namespace_user_subparser = namespace_user_parser.add_subparsers(
      dest="namespace_user_command", help="Subcommands of namespace_user")

  # subcommand of namespace_user: list
  namespace_user_list_parser = namespace_user_subparser.add_parser("list", help="List the namespace_user")
  namespace_user_list_parser.add_argument(
    "-n", "--namespace", dest="namespace", help="The name of the namespace")
  namespace_user_list_parser.set_defaults(func=util.list_namespace_user)

  # subcommand of namespace_user: add
  namespace_user_add_parser = namespace_user_subparser.add_parser(
      "add", help="Add namespace_user")
  namespace_user_add_parser.add_argument("namespace", help="The namespace to set")
  namespace_user_add_parser.add_argument(
      "user_ids", metavar="user_id", nargs="+", help="The ids of the user")
  namespace_user_add_parser.set_defaults(func=util.add_namespace_user)

  # subcommand of namespace_user: remove
  namespace_user_remove_parser = namespace_user_subparser.add_parser(
      "remove", help="Remove namespace_user")
  namespace_user_remove_parser.add_argument("namespace", help="The namespace to set")
  namespace_user_remove_parser.add_argument(
      "user_ids", metavar="user_id", nargs="+", help="The ids of the user")
  namespace_user_remove_parser.set_defaults(func=util.remove_namespace_user)


  args = parser.parse_args()
  args.func(args)


if __name__ == "__main__":
  main()
