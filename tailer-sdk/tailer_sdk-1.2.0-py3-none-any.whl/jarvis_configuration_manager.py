# -*- coding: utf-8 -*-

import os
import sys
import requests
import base64
import re

import shutil
import json
from pathlib import Path
from subprocess import check_output
import platform
import ctypes

from tailer_sdk import jarvis_config
from tailer_sdk import jarvis_auth
from tailer_sdk import jarvis_misc
from tailer_sdk import sql_dag_generator


def display_configuration_help(command, jarvis_configuration, firebase_user):

    try:

        # Get UID
        #
        uid = firebase_user["userId"]

        url = jarvis_configuration["jarvis_api_endpoint"] + \
            "configuration/v2/help"

        data = {
            "payload": {
                "resource_type": "help",
                "resource": command + "_help"
            }
        }

        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"]
        }

        r = requests.post(url, headers=headers, data=json.dumps(
            data), verify=jarvis_configuration["perform_ssl_verification"])

        if r.status_code != 200:
            print("\nError : %s\n" % str(r.content, "utf-8"))
        else:
            response = r.json()
            print(response["payload"]["help"])

    except Exception as ex:
        print("Error while trying to contact Jarvis API ...")
        print(ex)
        return False

    return True


def process_sql_query(read_configuration, input_conf_file):

    # Get path
    #
    filepath = os.path.dirname(input_conf_file)
    print("File path : {}".format(filepath))

    # Read associated SQL file
    #
    host_system = jarvis_misc.check_platform()

    path_element = None
    if (host_system == "Linux") or (host_system == "Darwin"):
        path_element = "/"
    elif host_system == "Windows":
        path_element = "\\"
    else:
        print("Host OS unknown, cannot process SQL file reading.")
        return None

    if (filepath is None) or (filepath == ""):
        sql_full_filename = read_configuration["sql_file"]
    else:
        sql_full_filename = filepath + path_element + \
            read_configuration["sql_file"]

    print("SQL file path : {}".format(sql_full_filename))

    try:

        # Read the content of the file, UTF-8 converted
        #
        read_sql_file = jarvis_misc.read_file_as_utf_8(sql_full_filename)

        # Convert SQL query into Base64
        #
        return str(base64.b64encode(read_sql_file), "utf-8")
    
    except Exception as ex:
        print("Error while reading SQL file : " + ex)
        
    return None


def process_configuration_file(input_conf_file, read_configuration=None):

    # Legacy mode
    #
    if read_configuration is None:

        # Check if the file exists
        #
        if os.path.isfile(input_conf_file) is False:
            print("File \"%s\" does not exists." % input_conf_file)
            return None

        # Read file and parse it as JSON
        #
        read_configuration = None
        try:

            # Read the content of the file, UTF-8 converted
            #
            file_read = jarvis_misc.read_file_as_utf_8(input_conf_file)

            read_configuration = json.loads(file_read)

        except Exception as ex:
            print("Error while parsing JSON configuration file : {}".format(input_conf_file))
            print(ex)
            return None

    # Add direct_execution if not present
    #
    try:
        direct_execution = read_configuration["direct_execution"]

        if type(direct_execution) is not bool:
            read_configuration["direct_execution"] = True

    except Exception:
        read_configuration["direct_execution"] = True

    # Get global path of the configuration file
    #
    configuration_absolute_pathname = jarvis_misc.get_path_from_file(
        input_conf_file)

    # Special processing for "table-to-storage"
    #
    if read_configuration["configuration_type"] == "table-to-storage":
        sql_query = process_sql_query(read_configuration, input_conf_file)
        if sql_query is None:
            return None

        read_configuration["sql"] = sql_query

    # Special processing for "storage-to-tables"
    #
    elif read_configuration["configuration_type"] == "storage-to-tables":

        # Process global Markdown file
        #
        try:
            doc_md = configuration_absolute_pathname + \
                read_configuration["doc_md"]

            print("Global Markdown file provided : {}".format(doc_md))
            try:
                with open(doc_md, "r") as f:
                    read_md_file = f.read()
                    read_md_file = bytes(read_md_file, "utf-8")
                    read_configuration["doc_md"] = str(
                        base64.b64encode(read_md_file), "utf-8")

            except Exception as ex:
                print("Error while reading Markdown file : " + ex)
                return None

        except KeyError:
            print("No global Markdown file provided. Continuing ...")

        # Process Destination
        #
        try:
            for destination in read_configuration["destinations"]:

                for table in destination["tables"]:

                    # Manage DDL Mode
                    #
                    # 3 modes are supported :
                    # file | header | file_template
                    #
                    # If mode is "file" the attribute "ddl_file" must be present
                    # If mode is "file_template", the attribute "ddl_file_template" must be present
                    #
                    if ("ddl_mode" not in table.keys()) or (table["ddl_mode"] == "file"):

                        try:

                            ddl_file = configuration_absolute_pathname + table["ddl_file"]
                            print("Processing DDL file : {}".format(ddl_file))

                            # Read the content of the file, UTF-8 converted
                            #
                            payload = jarvis_misc.read_file_as_utf_8(ddl_file)

                            # Try to parse the file as JSON to make sure there is no syntax error
                            #
                            json.loads(payload)

                            # Finally, Base 64 encode to get it ready for transfer
                            #
                            read_ddl_file = payload

                            table["ddl_infos"] = str(base64.b64encode(read_ddl_file), "utf-8")

                        except Exception as ex:
                            print("Error while parsing DDL file : {}".format(ddl_file))
                            print(ex)
                            return None

                    # Process Markdown file
                    # optional
                    #
                    try:
                        doc_md = configuration_absolute_pathname + table["doc_md"]
                        print("Processing table Markdown file : {}".format(doc_md))

                        # Read the content of the file, UTF-8 converted
                        #
                        read_doc_md = jarvis_misc.read_file_as_utf_8(doc_md)

                        table["doc_md"] = str(base64.b64encode(read_doc_md), "utf-8")

                    except Exception as ex:
                        print("Cannot process table Markdown file. Continuing ... : {}".format(ex))

        except Exception as ex:
            print("Error while processing destinations / tables : {}".format(ex))
            return None

    return read_configuration


def check_configuration(
        input_conf_file=None,
        jarvis_configuration=None,
        read_configuration=None,
        firebase_user=None):

    # Process configuration file
    #
    read_configuration = process_configuration_file(input_conf_file, read_configuration=read_configuration)

    # Call API
    #
    try:

        url = jarvis_configuration["jarvis_api_endpoint"] + "configuration/v2"
        data = {
            "payload": {
                "resource_type": "check-configuration",
                "resource": read_configuration,
                "uid": firebase_user["userId"]
            }
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"]}

        r = requests.post(url, headers=headers, data=json.dumps(
            data), cert=jarvis_configuration["client_ssl_certificate"], verify=jarvis_configuration["perform_ssl_verification"])

        if r.status_code == 404:
            # Special case : if the configuration JSON Schema is not found, we let pass until we can complete the JSON Schema database
            #
            print("\nConfiguration JSON Schema not found in JARVIS Platform.")
            return True
        elif r.status_code != 200:
            print("\nError(s) : \n%s\n" % str(r.content, "utf-8"))
            return False
        else:
            response = r.json()
            print(response["payload"]["message"])
            return True

    except Exception as ex:
        print("Error while trying to contact Jarvis API ...")
        print(ex)
        return False


def get_project_profile_from_configuration(
        input_conf_file=None,
        jarvis_configuration=None,
        read_configuration=None,
        firebase_user=None):

    # Process configuration file
    #
    if read_configuration is None:
        read_configuration = process_configuration_file(input_conf_file, read_configuration=read_configuration)

    # Call API
    #
    try:

        url = jarvis_configuration["jarvis_api_endpoint"] + "configuration/v2"
        data = {
            "payload": {
                "resource_type": "get-gcp-project-id",
                "resource": read_configuration,
                "uid": firebase_user["userId"]
            }
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"]}

        r = requests.post(url, headers=headers, data=json.dumps(
            data), verify=jarvis_configuration["perform_ssl_verification"])

        if r.status_code == 404:
            # Not found
            #
            print("\nGCP Project ID not found for your configuration")
            return None

        elif r.status_code != 200:
            print("\nError(s) : \n%s\n" % str(r.content, "utf-8"))
            return None

        else:
            response = r.json()
            return response["payload"]["message"]

    except Exception as ex:
        print("Error while trying to contact Jarvis API ...")
        print(ex)
        return None


def deploy_configuration(
        input_conf_file,
        jarvis_configuration,
        firebase_user,
        gcp_cf_deploy,
        project_profile=None,
        read_configuration=None,
        jarvis_sdk_version=None,
        no_dag_execution=False):

    # Process configuration file
    #
    if read_configuration is None:
        read_configuration = process_configuration_file(input_conf_file)

    # If project

    # Tag configuration with :
    # client_type
    # client_version
    #
    read_configuration["client_type"] = "jarvis-sdk"
    read_configuration["client_version"] = jarvis_sdk_version

    # Ask if the user wants to launch an execution upon successfull upload
    # Will work onmy for direct execution DAGs
    #
    execute_dag = False
    if no_dag_execution is False:
        try:
            if read_configuration["direct_execution"] is True:
                if read_configuration["configuration_type"] in ["vm-launcher"]:
                    while True:
                        print("Do you want to execute the DAG associated with your configuration ? y/n. Press enter for \"n\" : ", end='', flush=True)
                        user_value = input()

                        if len(user_value) == 0:
                            user_value = "n"

                        if user_value == "y":
                            execute_dag = True
                            break
                        elif user_value == "n":
                            execute_dag = False
                            break
        except Exception:
            execute_dag = False

    # Do we need to deploy the associated CF ?
    #
    if gcp_cf_deploy is True:
        print("\nThe GCP Cloud Function associated with your configuration deployment will be deployed if needed.")
        print("Please wait up to 2 minutes for full deployment.")
    else:
        print("\nThe GCP Cloud Function associated to your configuration WILL NOT be deployed.")

    # Call API
    #
    try:

        url = jarvis_configuration["jarvis_api_endpoint"] + "configuration/v2"
        data = {
            "payload": {
                "resource": read_configuration,
                "project_profile": project_profile,
                "uid": firebase_user["userId"],
                "deploy_cf": gcp_cf_deploy,
                "execute_dag": execute_dag
            }
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"
                                                       ]}

        r = requests.put(url, headers=headers, data=json.dumps(
            data), verify=jarvis_configuration["perform_ssl_verification"])

        if r.status_code != 200:
            print("\nError : %s\n" % str(r.content, "utf-8"))
            return False
        else:
            response = r.json()
            print(response["payload"]["message"])
            return True

    except Exception as ex:
        print("Error while trying to contact Jarvis API ...")
        print(ex)
        return False


def create_configuration(configuration_type, output_file, jarvis_configuration, firebase_user):

    # Some information
    #
    print("Configuration type : {}".format(configuration_type))
    print("Output file        : {}".format(output_file))

    # Call API
    #
    try:

        url = jarvis_configuration["jarvis_api_endpoint"] + "configuration/v2"
        data = {
            "payload": {
                "resource_type": "configuration-type",
                "resource": configuration_type,
                "uid": firebase_user["userId"]
            }
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"
                                                       ]}

        r = requests.post(url, headers=headers, data=json.dumps(
            data), verify=jarvis_configuration["perform_ssl_verification"])

        if r.status_code != 200:
            print("\nError : %s\n" % str(r.content, "utf-8"))
            return False
        else:
            response = r.json()
            config = str(base64.b64decode(
                response["payload"]["content"]), "utf-8")
            with open(output_file, mode='w') as file:
                file.write(config)
            return True

    except Exception as ex:
        print("Error while trying to contact Jarvis API ...")
        print(ex)
        return False


def check_table_to_table(input_configuration):

    # Process configuration file
    #
    read_configuration = process_configuration_file(input_configuration)
    if read_configuration is None:
        return False

    try:
        if read_configuration["configuration_type"] == "table-to-table":
            return True
    except Exception as ex:
        print("Error while parsing configuration file.")
        print(ex)

    return False


def check_sts_or_stt(input_configuration):

    # Process configuration file
    #
    read_configuration = process_configuration_file(input_configuration)
    if read_configuration is None:
        return False

    try:
        if (read_configuration["configuration_type"] == "storage-to-storage") or (read_configuration["configuration_type"] == "storage-to-tables"):
            return True
    except Exception as ex:
        print("Error while parsing configuration file.")
        print(ex)

    return False


def process_cf_deployment(input_configuration, jarvis_configuration, no_gcp_cf_deploy):

    
    if no_gcp_cf_deploy is True:

        return False

    else:

        if check_sts_or_stt(input_configuration) is True:

            try:
                if jarvis_configuration["cf_deploy_auto_sts_stt"] is True:
                    return True
            except:
                noop = 1

            # If we are here, we need to ask the user
            #
            while True:
                print("Do you want to perform the deployment of the associated Cloud Function ? y/n. Press enter for \"y\" : ", end='', flush=True)
                user_value = input()

                if len(user_value) == 0:
                    user_value = "y"

                if user_value == "y":
                    return True
                elif user_value == "n":
                    return False

        else:

            return True


def get_configuration_version(input_configuration):

    # Process configuration file
    #
    read_configuration = process_configuration_file(input_configuration)
    if read_configuration is None:
        return "1"

    try:
        return read_configuration["version"]
    except Exception:
        return "1"


def process_project_profile(
        input_conf_file,
        jarvis_configuration,
        firebase_user):

    project_profile = get_project_profile_from_configuration(
                        input_conf_file=input_conf_file,
                        jarvis_configuration=jarvis_configuration,
                        firebase_user=firebase_user)

    if (project_profile is None) or (project_profile == ""):

        # Get list of project profiles open to the user and ask him to pick one
        #
        ret_code, project_profile = jarvis_misc.choose_project_profiles(
            jarvis_configuration, firebase_user)
        if ret_code is False:
            return None

    else:
        print("\nProject profile used : {}\n".format(
            project_profile))

    return project_profile


def process_configuration_context(
        input_configuration,
        jarvis_configuration,
        firebase_user,
        context_choice=None):

    # Read RAW configuration
    #
    read_configuration = process_configuration_file(input_configuration)
    if read_configuration is None:
        return False, None

    # Check oif a context has been specified on command lien.
    #
    if context_choice is None:
        # Ask the user to choose the project context
        # Only available context will be presented
        #
        ret_code, context_choice = jarvis_misc.choose_context(
                                        jarvis_configuration=jarvis_configuration,
                                        firebase_user=firebase_user)

        if ret_code is False:
            return False, None

        # No context management
        #
        if context_choice.strip() == "NO_CONTEXT":
            return True, None

    # Send back the choice to Tailer API and return the project context
    #
    ret_code, context_data = jarvis_misc.retrieve_context(
                                jarvis_configuration=jarvis_configuration,
                                firebase_user=firebase_user,
                                context_id=context_choice.strip())

    if ret_code is False:
        return False, None

    # Transform configuration to string
    #
    configuration_string = json.dumps(read_configuration, indent=4)

    # Parse the user's configuration file and apply context
    #
    try:
        configuration_string = configuration_string.replace("{{FD_ENV}}", context_data["environment"])
        configuration_string = configuration_string.replace("{{FD_ACCOUNT}}", context_data["account"])

        # Regular variables
        #
        regex = """\"{{([^{]*)}}\""""
        result = re.findall(regex, configuration_string)
        
        for variable in result:
            try:
                print("Parsing variable : {}".format(variable))
                configuration_string = configuration_string.replace("""\"{{""" + variable + """}}\"""", json.dumps(context_data["parameters"][variable]["value"], indent=4))
            except Exception:
                pass

        # Variables embedded within strings
        # This will replace STRING, INT and FLOAT types only
        #
        regex = """{{([^{]*)}}"""
        result = re.findall(regex, configuration_string)
        
        for variable in result:
            try:
                print("Parsing variable : {}".format(variable))
                if context_data["parameters"][variable]["type"] in ["string", "integer", "float"]:
                    configuration_string = configuration_string.replace("""{{""" + variable + """}}""", json.dumps(context_data["parameters"][variable]["value"], indent=4).replace("\"",""))
                else:
                    configuration_string = configuration_string.replace("""{{""" + variable + """}}""", "VARIABLE_TYPE_NOT_SUPPORTED_PLEASE_CHECK_CONTEXT")

            except Exception as ex:
                print("Error while applying context on the configuration : {}".format(str(ex)))
                pass

        read_configuration = json.loads(configuration_string)

        # Process configuration ID and configuration name
        #
        read_configuration["configuration_name"] = read_configuration["configuration_id"]
        read_configuration["configuration_id"] = read_configuration["account"].strip() + "_" + context_data["configuration_id"].strip() + "_" + read_configuration["configuration_id"].strip()

    except Exception as ex:
        print("Error while parsing configuration : {}".format(str(ex)))
        return False, None

    return True, read_configuration


def process(args, jarvis_sdk_version):

    print("Jarvis Configuration Manager.")

    # Get configuration
    #
    jarvis_configuration = jarvis_config.get_jarvis_configuration_file()

    # Get firebase user
    #
    firebase_user = jarvis_auth.get_refreshed_firebase_user(
        jarvis_configuration)

    if args.command == "deploy":
        if len(args.arguments) >= 2:
            if args.arguments[1] is not None:
                if args.arguments[1] == "help":
                    return display_configuration_help(args.command, jarvis_configuration, firebase_user)
                else:

                    # # Special check for TABLE-TO-TABLE (DAG Generator) configuration
                    # # If so, we need to process the configuration file
                    # #
                    # if check_table_to_table(args.arguments[1]) is True:
                    #     print("Processing table-to-table type configuration ...")
                    #     sql_dag_generator.process(
                    #         configuration_file=args.arguments[1], jarvis_sdk_version=jarvis_sdk_version)
                    #     return True

                    # Get optional flags
                    #
                    cmd_line_context = None
                    cmd_line_no_launch = False

                    for remainder_index in range(2,len(args.arguments)):

                        if args.arguments[remainder_index].strip() == "--context":
                            try:
                                cmd_line_context = args.arguments[remainder_index + 1].strip()
                            except Exception:
                                print("\nError : Please specify a context.\n")
                                return False

                        elif args.arguments[remainder_index].strip() == "--no-launch":
                            cmd_line_no_launch = True

                    # Retrieve configuration version
                    #
                    configuration_version = get_configuration_version(input_configuration=args.arguments[1])
                    print("Configuration version : {}".format(configuration_version))

                    # Process context for configuration version >= 2
                    #
                    read_configuration = None
                    if configuration_version == "2":
                        ret_code, read_configuration = process_configuration_context(
                                                            input_configuration=args.arguments[1],
                                                            jarvis_configuration=jarvis_configuration,
                                                            firebase_user=firebase_user,
                                                            context_choice=cmd_line_context)
                        if ret_code is False:
                            print("Error while processing configuration context.")
                            return False

                    # DEBUG
                    #
                    try:
                        print("Configuration id : {}".format(read_configuration["configuration_id"]))
                    except Exception:
                        pass

                    # Special check for TABLE-TO-TABLE (DAG Generator) configuration
                    # If so, we need to process the configuration file
                    #
                    if check_table_to_table(args.arguments[1]) is True:
                        print("Processing table-to-table type configuration ...")
                        sql_dag_generator.process(
                            configuration_file=args.arguments[1],
                            read_configuration=read_configuration,
                            jarvis_sdk_version=jarvis_sdk_version)
                        return True

                    # Check if the configuration is valid
                    #
                    if check_configuration(
                            input_conf_file=args.arguments[1],
                            jarvis_configuration=jarvis_configuration,
                            read_configuration=read_configuration,
                            firebase_user=firebase_user) is False:

                        return False

                    # Process Cloud Function deployment
                    #
                    # Only for STS and STT
                    #
                    gcp_cf_deploy = process_cf_deployment(input_configuration=args.arguments[1], jarvis_configuration=jarvis_configuration, no_gcp_cf_deploy=args.no_gcp_cf_deploy)

                    # Check if GCP Project ID is present
                    #
                    project_profile = None
                    if (configuration_version == "1") or (read_configuration is None):

                        project_profile = process_project_profile(
                                            input_conf_file=args.arguments[1],
                                            jarvis_configuration=jarvis_configuration,
                                            firebase_user=firebase_user)

                        if project_profile is None:
                            return False

                    else:

                        project_profile = get_project_profile_from_configuration(
                                            input_conf_file=args.arguments[1],
                                            jarvis_configuration=jarvis_configuration,
                                            read_configuration=read_configuration,
                                            firebase_user=firebase_user)

                        if project_profile is None:
                            return False

                    print("Attempting to deploy regular configuration...")

                    # DEBUG
                    #
                    try:
                        print("Configuration id : {}".format(read_configuration["configuration_id"]))
                    except Exception:
                        pass

                    return deploy_configuration(
                                args.arguments[1],
                                jarvis_configuration,
                                firebase_user,
                                gcp_cf_deploy,
                                project_profile=project_profile,
                                read_configuration=read_configuration,
                                jarvis_sdk_version=jarvis_sdk_version,
                                no_dag_execution=cmd_line_no_launch)

            else:
                print("Argument unknown." % args.arguments[1])
                return False
        else:
            return display_configuration_help(args.command, jarvis_configuration, firebase_user)

    elif args.command == "create":
        if len(args.arguments) >= 2:
            if args.arguments[1] is not None:
                if args.arguments[1] == "help":
                    return display_configuration_help(args.command, jarvis_configuration, firebase_user)
                else:

                    # retrieve output_filename
                    #
                    try:
                        output_filename = args.arguments[2]
                    except Exception:
                        output_filename = args.arguments[1] + ".json"

                    return create_configuration(args.arguments[1], output_filename, jarvis_configuration, firebase_user)
            else:
                print("Argument unknown." % args.arguments[1])
                return False
        else:
            return display_configuration_help(args.command, jarvis_configuration, firebase_user)

    elif args.command == "check":
        if len(args.arguments) >= 2:
            if args.arguments[1] is not None:
                if args.arguments[1] == "help":
                    return display_configuration_help(args.command, jarvis_configuration, firebase_user)
                else:
                    return check_configuration(input_conf_file=args.arguments[1], jarvis_configuration=jarvis_configuration, firebase_user=firebase_user)
            else:
                print("Argument unknown." % args.arguments[1])
                return False
        else:
            return display_configuration_help(args.command, jarvis_configuration, firebase_user)

    return True
