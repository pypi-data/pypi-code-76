# -*- coding: utf-8 -*-

import os
import sys
import requests

import shutil
import json
from pathlib import Path
from subprocess import check_output
import platform
import ctypes

from tailer_sdk import tailer_config
from tailer_sdk import tailer_auth
from tailer_sdk import tailer_misc


def display_gcp_cf_deploy_help(
        deploy_configuration,
        firebase_user):

    try:

        # Get UID
        #
        uid = firebase_user["userId"]

        # Get default project
        #
        default_project = (tailer_config.get_tailer_configuration_file())["gcp_default_project"]

        url = deploy_configuration["deploy_api_endpoint"] + "gcp-cloud-function/v2/help"
        data = {
            "payload": {
                "resource": "help",
                "uid" : uid,
                "gcp_project_id" : default_project
            }
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"]
        }

        r = requests.post(url, headers=headers, data=json.dumps(data), verify=deploy_configuration["perform_ssl_verification"])

        if r.status_code != 200:
            # print(r.headers)
            print("\nError : %s\n" % str(r.content, "utf-8"))
        else:
            response = r.json()
            print(response["payload"]["help"])

    except Exception as ex:
        print("Error while trying to contact Deploy API ...")
        print(ex)
        return False

    return True


def display_gcp_cf_deploy(
        project_profile,
        tailer_configuration,
        firebase_user,
        arguments):

    # Infos
    #
    print("Deploying GCP Cloud Function. Please wait up to 2 minutes ...")

    # Call API
    #
    try:

        url = tailer_configuration["tailer_api_endpoint"] + "gcp-cloud-function/v2"
        data = {
            "payload": {
                "resource": arguments,
                "project_profile": project_profile,
                "uid" : firebase_user["userId"],
            }
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"]}

        r = requests.put(
                url,
                headers=headers,
                data=json.dumps(data),
                verify=tailer_configuration["perform_ssl_verification"])

        if r.status_code != 200:
            print("\nError : %s\n" % str(r.content, "utf-8"))
            return False
        else:
            response = r.json()
            print(response["payload"]["message"])
            return True

    except Exception as ex:
        print("Error while trying to contact Tailer API ...")
        print(ex)
        return False


def process(args):

    print("Tailer Configuration Manager.")

    # Get configuration
    #
    tailer_configuration = tailer_config.get_tailer_configuration_file()

    # Get firebase user
    #
    firebase_user = tailer_auth.get_refreshed_firebase_user(tailer_configuration)

    if args.command == "deploy":
        if len(args.arguments) >= 2:
            if args.arguments[0] == "gcp-cloud-function":
                if args.arguments[1] is not None:
                    if args.arguments[1] == "help":
                        return display_gcp_cf_deploy_help(tailer_configuration, firebase_user)
                    else:
                        # Get list of project profiles open to the user and ask him to pick one
                        #
                        ret_code, project_profile = tailer_misc.choose_project_profiles(tailer_configuration, firebase_user)
                        if ret_code is False:
                            return False
                        return display_gcp_cf_deploy(project_profile, tailer_configuration, firebase_user, args.arguments[1:])
                else:
                    print("Argument unknown." % args.arguments[1])
                    return False
            else:
                    print("Argument unknown." % args.arguments[0])
                    return False
        else:
            return display_gcp_cf_deploy_help(tailer_configuration, firebase_user)

    return True
