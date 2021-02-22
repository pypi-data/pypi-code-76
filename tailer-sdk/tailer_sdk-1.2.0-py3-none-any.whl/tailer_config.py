# -*- coding: utf-8 -*-

import os
import sys
import shutil
import json
from pathlib import Path
from subprocess import check_output
import platform
import ctypes

from tailer_sdk import tailer_misc


# Globals
#
_tailer_rc_file_ = "tailerrc"
_tailer_configuration_file_ = "tailer-configuration.json"
_tailer_default_parameters_ = {
    "user_email": {
        "name": "Your email address",
        "value": ""
    },
    "tailer_firebase_api_key": {
        "name": "Tailer Firebase API key",
        "value": ""
    },
    "tailer_firebase_auth_domain": {
        "name": "Tailer Firebase Authentication Domain",
        "value": ""
    },
    "tailer_api_endpoint": {
        "name": "Tailer API Endpoint",
        "value": ""
    }
}


def get_tailer_home():

    # Get host system
    #
    host_system = tailer_misc.check_platform()

    if (host_system == "Linux") or (host_system == "Darwin"):
        return os.environ["TAILER_HOME"] + "/"
    elif host_system == "Windows":
        return os.environ["TAILER_HOME"] + "\\"
    else:
        return None


def set_tailer_configuration_file(data):

    # Get host system
    #
    host_system = tailer_misc.check_platform()

    tailer_configuration_file_full_path = None
    if (host_system == "Linux") or (host_system == "Darwin"):
        tailer_configuration_file_full_path = os.environ["TAILER_HOME"] + \
            "/" + _tailer_configuration_file_
    elif host_system == "Windows":
        tailer_configuration_file_full_path = os.environ["TAILER_HOME"] + \
            "\\" + _tailer_configuration_file_
    else:
        print("Host OS unknown, cannot process Tailer configuration file.")
        return False

    with open(tailer_configuration_file_full_path, "w") as f:
        json.dump(data, f)


def get_tailer_configuration_file(create_if_not_exists=False):

    # Get host system
    #
    host_system = tailer_misc.check_platform()

    tailer_configuration_file_full_path = None
    if (host_system == "Linux") or (host_system == "Darwin"):
        tailer_configuration_file_full_path = os.environ["TAILER_HOME"] + \
            "/" + _tailer_configuration_file_
    elif host_system == "Windows":
        tailer_configuration_file_full_path = os.environ["TAILER_HOME"] + \
            "\\" + _tailer_configuration_file_
    else:
        print("Host OS unknown, cannot process Tailer configuration file.")
        return False

    # Check that file exists
    #
    if (os.path.isfile(tailer_configuration_file_full_path) is False) and (create_if_not_exists is True):

        # Create file
        #
        with open(tailer_configuration_file_full_path, "w") as f:
            print("Creating {}".format(tailer_configuration_file_full_path))
            f.write("{}\n")

    # Read/write file content
    #
    read_configuration = None
    try:
        with open(tailer_configuration_file_full_path, "r") as f:
            read_configuration = json.load(f)
    except Exception as ex:
        print("Error during configuration reading/parsing.")
        print(ex)

    # Check for non-present values
    #
    if "perform_ssl_verification" not in read_configuration:
        read_configuration["perform_ssl_verification"] = False

    if "client_ssl_certificate" not in read_configuration:
        read_configuration["client_ssl_certificate"] = ""

    # Make sur those variables are set
    #
    # SSL_CERT_FILE
    #
    if read_configuration["client_ssl_certificate"] is not None:
        os.environ["SSL_CERT_FILE"] = read_configuration["client_ssl_certificate"]
    else:
        del os.environ["SSL_CERT_FILE"]

    print("SSL Cert. : {}".format(os.environ["SSL_CERT_FILE"]))

    return read_configuration


def check_administrator(host_system):

    print("Checking if we run in ROOT / ADMINISTRATOR mode...")

    if (host_system == "Darwin") or (host_system == "Linux"):

        if os.getuid() == 0:

            # You are ROOT
            print("ERROR : Please DO NOT run install as ROOT. Exiting")
            return True
        else:
            return False

    elif (host_system == "Windows"):

        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            return False
        else:
            # ADMIN privileges
            #
            print("WARNING : you are running this script with ADMINISTRATOR privileges.")
            # return True

            # Under Windows, it's ok ...
            return False

    else:

        print("Host system unknown, assuming you are not ROOT / ADMIN")
        return False


def process_tailer_home_directory(host_system):

    tailer_homedir_suffix = None

    if (host_system == "Linux") or (host_system == "Darwin"):
        print("Processing Tailer Home directory for Mac OS X / Linux ...")
        tailer_homedir_suffix = "/.tailer-home"
    elif host_system == "Windows":
        print("Processing Tailer Home directory for Windows OS ...")
        tailer_homedir_suffix = "\AppData\Local\tailer-home"
    else:
        print("Host OS unknown, cannot process Tailer Home directory")
        return None

    # Check if directory exists, create it if needed
    #
    tailer_homedir = str(Path.home()) + tailer_homedir_suffix
    if os.path.exists(tailer_homedir) is True:
        print("Tailer home directory found : " + tailer_homedir)
        return tailer_homedir
    else:
        # Create directory
        #
        try:
            os.mkdir(tailer_homedir)
        except OSError:
            print("Creation of the directory {} failed".format(tailer_homedir))
            return None
        else:
            print("Successfully created the directory {} ".format(tailer_homedir))
            return tailer_homedir


def process_tailer_home_env_variable(host_system):

    if (host_system == "Linux") or (host_system == "Darwin"):
        print("Processing Tailer Home directory for Mac OS X / Linux ...")

        user_rc_file = None
        if host_system == "Linux":
            user_rc_file = ".bashrc"
        elif host_system == "Darwin":

            # Check the SHELL used
            #
            user_rc_file = ".bash_profile"
            try:
                if "zsh" in os.environ["SHELL"]:
                    user_rc_file = ".zshrc"
            except Exception:
                print("Shell does not seem to be ZSH.")

        # Home directory
        #
        user_rc_file_full_path = (
            os.getenv("HOME")).strip() + "/" + user_rc_file
        print("User RC file : {}".format(user_rc_file_full_path))

        # Check that file exists
        #
        if os.path.isfile(user_rc_file_full_path) is False:
            print("WARNING : User rc file \"{}\" not found. Let's create it.".format(user_rc_file_full_path))
            with open(user_rc_file_full_path, "w") as f:
                print("{} successfully created.".format(user_rc_file_full_path))

        # Remove the TAILER SDK lines
        #
        tailerrc_file_full_path = os.environ["TAILER_HOME"] + "/" + _tailer_rc_file_
        with open(user_rc_file_full_path, "r") as f:
            lines = f.readlines()
        with open(user_rc_file_full_path, "w") as f:
            for line in lines:
                if ("#TAILER SDK" not in line) and (_tailer_rc_file_ not in line):
                    f.write(line)

            # Adding the lines
            #
            f.write("#TAILER SDK\n")
            f.write("if [ -f '" + tailerrc_file_full_path +
                    "' ]; then . '" + tailerrc_file_full_path + "'; fi\n")

        # Write "tailerrc" file
        #
        with open(tailerrc_file_full_path, "w") as f:
            f.write("export TAILER_HOME=" + os.environ["TAILER_HOME"] + "\n")

    elif host_system == "Windows":
        print("Processing Tailer Home environment variable for Windows OS ...")

        windows_set_env_variable = "setx TAILER_HOME \"" + os.environ["TAILER_HOME"] + "\""
        check_output(windows_set_env_variable, shell=True)

    else:
        print("Host OS unknown, cannot process Tailer Home environment variable.")
        return False

    return True


def process_configuration_file(host_system):

    read_configuration = get_tailer_configuration_file(create_if_not_exists=True)

    if read_configuration is None:
        return False

    # Going through default parameters
    #
    print()
    for key in _tailer_default_parameters_.keys():

        built_message = "Please provide " + \
            _tailer_default_parameters_[key]["name"] + \
            ". Actual/default value => {} : "

        actual_or_default_value = None
        value_if_empty = None
        try:
            actual_or_default_value = read_configuration[key]
            value_if_empty = read_configuration[key]
        except KeyError:
            actual_or_default_value = _tailer_default_parameters_[key]["value"]
            value_if_empty = _tailer_default_parameters_[key]["value"]

        # Display request to the user
        #
        print(built_message.format(actual_or_default_value), end='', flush=True)

        # Get user value
        #
        user_value = input()

        if not user_value:
            # If the user just hit enter, we'll use the actual/default value
            #
            read_configuration[key] = value_if_empty
        else:
            read_configuration[key] = user_value

    # Process SSL Bypass
    #
    while True:
        print("Do you want to perform the SSL verification ? y/n. Press enter for \"y\" : ", end='', flush=True)
        user_value = input()

        if len(user_value) == 0:
            user_value = "y"

        if user_value == "y":
            read_configuration["perform_ssl_verification"] = True
            break
        elif user_value == "n":
            read_configuration["perform_ssl_verification"] = False
            break

    # Process Client SSL certificate
    #
    while True:
        print("Do you want to specify a custom Client SSL Certificate ? y/n. Press enter for \"n\" : ", end='', flush=True)
        user_value = input()

        if len(user_value) == 0:
            user_value = "n"

        if user_value == "y":
            print("\n--> Please provide full path to your SSL certificate : ", end='', flush=True)
            user_value = input()
            read_configuration["client_ssl_certificate"] = user_value
            break
        elif user_value == "n":
            read_configuration["client_ssl_certificate"] = ""
            break

    # Process automatic deployment for STS and STT Cloud Functions
    #
    while True:
        print("Do you want to perform automatic deployment of STS and STT associated Cloud Functions ? y/n. Press enter for \"y\" : ", end='', flush=True)
        user_value = input()

        if len(user_value) == 0:
            user_value = "y"

        if user_value == "y":
            read_configuration["cf_deploy_auto_sts_stt"] = True
            break
        elif user_value == "n":
            read_configuration["cf_deploy_auto_sts_stt"] = False
            break

    # Write file out
    #
    set_tailer_configuration_file(read_configuration)

    return True


def tailer_config():

    print("Installing Tailer SDK ...")

    # Step 1 : check platform
    #
    host_system = tailer_misc.check_platform(print_infos=True)

    # Step 2 : check SUDO / ADMINISTRATOR execution
    # Darwin, Linux, Windows, ...
    #
    if check_administrator(host_system) is True:
        return False

    # Step 3 : manage "tailer sdk" directory
    #
    tailer_home_directory = process_tailer_home_directory(host_system)

    # Set temporarily the env. variable
    #
    os.environ["TAILER_HOME"] = tailer_home_directory

    if tailer_home_directory is None:
        print("ERROR while processing Tailer home directory. Please check console output. Exiting.")
        return False

    # Step 4 : manage TAILER_HOME environment variable
    #
    if process_tailer_home_env_variable(host_system) is not True:
        print("ERROR while processing Tailer home environment variable. Please check console output. Exiting.")
        return False

    # Step 5 : create/update configuration file
    #
    if process_configuration_file(host_system) is False:
        print("Error while creating/upgrading configuration file.")

    # Final step
    #
    print("\nTailer SDK installation is now complete. Please exit and re-launch your terminal.\n")

    return True


def check_jarvis_home_directory(host_system):

    jarvis_homedir_suffix = None

    if (host_system == "Linux") or (host_system == "Darwin"):
        print("Processing Jarvis Home directory for Mac OS X / Linux ...")
        jarvis_homedir_suffix = "/.jarvis-home"
    elif host_system == "Windows":
        print("Processing Jarvis Home directory for Windows OS ...")
        jarvis_homedir_suffix = "\AppData\Local\jarvis-home"
    else:
        print("Host OS unknown, cannot process Jarvis Home directory")
        return None

    # Check if directory exists, create it if needed
    #
    jarvis_homedir = str(Path.home()) + jarvis_homedir_suffix
    if os.path.exists(jarvis_homedir) is True:
        print("Jarvis home directory found : " + jarvis_homedir)
        return jarvis_homedir
    else:
        return None


def migrate_jarvis_config_files(
        jarvis_home_directory,
        tailer_home_directory,
        host_system):

    # Copy jarvis_public_key.pem -> tailer_public_key.pem
    #
    try:
        if (host_system == "Linux") or (host_system == "Darwin"):
            source_file = "/.jarvis-home/jarvis_public_key.pem"
            destination_file = "/.tailer-home/tailer_public_key.pem"
        elif host_system == "Windows":
            source_file = "\AppData\Local\jarvis-home\jarvis_public_key.pem"
            destination_file = "\AppData\Local\tailer-home\tailer_public_key.pem"
        else:
            print("Host OS unknown, cannot process migration from Jarvis SDK")
            return False

        shutil.copyfile(
                str(Path.home()) + source_file,
                str(Path.home()) + destination_file)
        print("Jarvis public key has been migrated to Tailer.")

    except Exception:
        print("Warning, Jarvis public key has not been migrated.")
        return True

    # Attempting to migrate the users configuration file
    #
    try:
        if (host_system == "Linux") or (host_system == "Darwin"):
            source_file = "/.jarvis-home/jarvis-configuration.json"
            destination_file = "/.tailer-home/tailer-configuration.json"
        elif host_system == "Windows":
            source_file = "\AppData\Local\jarvis-home\jarvis-configuration.json"
            destination_file = "\AppData\Local\tailer-home\tailer-configuration.json"
        else:
            print("Host OS unknown, cannot process migration from Jarvis SDK")
            return False

        with open(str(Path.home()) + source_file, "r") as input_json_file:
            input_configuration = json.loads(input_json_file.read())
            
        output_configuration = {}
        for key in input_configuration.keys():

            print("Processing key : {} ...".format(key))
            newkey = key.replace("jarvis", "tailer")
            output_configuration[newkey] = input_configuration[key]

        # Set file
        #
        set_tailer_configuration_file(output_configuration)

    except Exception as ex:
        print("Warning, User configuration file will not be migrated : {}".format(ex))
        return True

    return True


def migrate_config():

    print("Migrating to Tailer SDK ...")

    # Step 1 : check platform
    #
    host_system = tailer_misc.check_platform(print_infos=True)

    # Step 2 : check SUDO / ADMINISTRATOR execution
    # Darwin, Linux, Windows, ...
    #
    if check_administrator(host_system) is True:
        return False

    # Step 3 :  check if jarvis-home exists
    #
    jarvis_home_directory = check_jarvis_home_directory(host_system)
    if jarvis_home_directory is None:
        return False

    # Step 4 : manage "tailer sdk" directory
    #
    tailer_home_directory = process_tailer_home_directory(host_system)

    # Set temporarily the env. variable
    #
    os.environ["TAILER_HOME"] = tailer_home_directory

    # Step 5 : attempt to migrate config files
    #
    if migrate_jarvis_config_files(
            jarvis_home_directory,
            tailer_home_directory,
            host_system) is False:
        return False

    # Step 6 : RC files and Env variables
    #
    if process_tailer_home_env_variable(host_system) is False:
        return False