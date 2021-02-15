"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""

NANO_SECONDS_OFFSET: float = 10 ** 9


class KSDKHelpMessages:
    # welcome message
    ksdk_welcome_message: str = """    Kelvin SDK:  The complete tool to interact with the Kelvin Ecosystem."""
    # ksdk help
    verbose: str = "Display all executed steps to the screen."
    yes: str = "If specified, will ignore the destructive warning of the operation and proceed."
    docs: str = "Open the kelvin-sdk documentation webpage."
    tree_title: str = """
        Kelvin Command Overview.
    """
    tree_help: str = "Display all available commands in a tree structure."
    current_system_info: str = "Provide system information and the currently logged platform."
    current_session_login: str = "No current session available."
    # login
    login_username: str = "The username used to login on the platform."
    login_password: str = "The password corresponding to the provided user."
    login_totp: str = "The time-based one-time password (TOTP) corresponding to the provided user."
    reset: str = "If specified will reset all local configuration files required by this tool."
    token_full: str = "Return the full authentication token, not just the access authentication token field."
    token_margin: str = """
        Minimum time to expiry (in seconds) for authentication token (new authentication_token retrieved if previous authentication token expires within margin).
        \b
        Set to 0 to retrieve a new authentication_token.
    """
    # applications
    app_description: str = "A simple description for the new app."
    app_type: str = """
        Specify the application type. \n
        Default: "kelvin"
    """
    kelvin_app_lang: str = """
        The programming language of the application.
        Applicable only to applications of type "kelvin". \n
        Default: "python"
    """
    kelvin_app_interface: str = """
        Specify the interface for the new application.
        Applicable only to applications of type "kelvin". \n
        Default: "data"
    """
    kelvin_app_flavour: str = """
        Specify the initial template styles.
        Applicable only to applications of type "kelvin". \n
        Default: "kelvin-app"
    """
    app_dir: str = "The path to the application's directory. Assumes the current directory if not specified."
    status_source: str = """
        The source of data to read from.
        Retrieve from 'cache' or force a 'live' update. \n
        Default: 'cache'.
    """
    # apps
    appregistry_show_app_version: str = "The app version to show."
    appregistry_delete_app_version: str = "The app version to delete. If not specified, deletes the app entirely."
    appregistry_download_override_local_tag: str = "If specified, overrides the local image tag."
    appregistry_upload_datamodels_upload: str = "If specified, will upload locally defined datamodels."
    # bundles
    bundle_app_config: str = "The app bundle configuration file to process."
    # workload list
    workload_list_acp_name: str = "The acp name used to filter the workloads."
    workload_list_app_name: str = "The app name used to filter the workloads."
    workload_list_app_version: str = "The app version used to filter the workloads."
    workload_list_enabled: str = "Allows the filtering of workloads by their status."
    # workload deploy
    workload_deploy_acp_name: str = "The acp to associate to the new workload."
    workload_deploy_app_name: str = "The app to associate to the new workload."
    workload_deploy_app_version: str = "The app version to associate to the new workload."
    workload_deploy_workload_name: str = "The name of the workload."
    workload_deploy_workload_title: str = "The title of the workload."
    workload_deploy_app_config: str = "The configuration file used to set up the workload."
    # workload bulk-deploy
    workload_deploy_bulk_file_type: str = "Type of the workload file."
    workload_deploy_bulk_ignore_failures: str = "Ignore deployment failures and automatically continue."
    workload_deploy_bulk_skip_successes: str = "Skip deployments already marked as successful."
    workload_deploy_bulk_dry_run: str = "Dry-run to validate inputs only."
    # workload update
    workload_update_app_version: str = "The app version to update the workload with."
    workload_update_workload_title: str = "The new title of the workload."
    workload_update_app_config: str = "The new configuration to be set on the existing workload."
    # workload logs
    workload_logs_tail_lines: str = "The number of lines to display."
    workload_logs_output_file: str = "The output file to write the logs into."
    workload_logs_follow: str = "If specified, follows the logs."
    # storage
    storage_acp_name: str = "The name of the ACP to filter the search."
    storage_source: str = "The source of data."
    storage_key: str = "The key to query for."
    storage_type: str = "The data type to query for."
    storage_start_date: str = """
        The start date to filter the search.

        \b
        Formats accepted:

        \b
        - ISO-8601 datetime with optional timezone, e.g.
            2020-04-09T09:01:59 (asumed to be in local timezone)
            2020-04-09T09:01:59+10:00 (specific timezone)
          Note: the T separator is optional and can be replaced with a space

        \b
        - UNIX timestamp in seconds since 1970-01-01T00:00:00+00:00, e.g.
            1586422919.0 (2020-04-09T09:01:59+00:00)

        \b
        """
    storage_end_date: str = "End date to filter the search."
    storage_agg: str = "The aggregate to filter the search."
    storage_time_bucket: str = "The time window over which to aggregate values."
    storage_time_shift: str = "The time period offset step for the time-bucket."
    storage_output_file: str = "The file into which the data will be saved."
    storage_output_format: str = "The file format for the saved data. 'json' is the default."
    storage_pivot: str = "Pivot keys into columns."
    # datamodel list
    datamodel_list_all: str = "If specified, will list all datamodels and its respective versions."
    # datamodel create
    datamodel_create_input_dir: str = "The directory to read the datamodels from."
    datamodel_create_output_dir: str = "The directory where the new data model will be created."
    # datamodel show
    datamodel_show_version: str = "The version of the data model to show."
    # datamodel upload
    datamodel_upload_input_dir: str = "The directory to read the datamodels from."
    datamodel_upload_names: str = "The data model names to filter the upload operation."
    # datamodel download
    datamodel_download_output_dir: str = "The directory where the downloaded data model will be put."
    # datamodel extract-schema
    datamodel_extract_schema_input_dir: str = "The directory where the data models are held."
    datamodel_extract_schema_output_dir: str = "The directory where the schemas will be placed."
    datamodel_extract_schema_names: str = "The data model names to filter the schema extraction operation."
    # emulation
    fresh: str = "If specified will remove any cache and rebuild the application from scratch."
    shared_dir: str = "The path to the directory shared between application container and host machine."
    show_logs: str = "Log the application's output once started."
    entry_point: str = "The entrypoint command to invoke the test."
    test_interactive: str = "Run the command interactively (not supported in Windows)"
    net_alias: str = "Network alias to provide alternate hostname on network (defaults to {app_name}.app)"
    port_mapping: str = """
        Specifies the port mapping between container and host.\n
        Format: <container-port:host-port>.\n
        E.g. 48010:48012.
    """
    emulation_logs_tail_lines: str = "Tails the container logs."
    emulation_app_config: str = "The app configuration file to be used on the emulation."
    # studio
    studio_schema_file: str = "The schema file used to power the Kelvin Studio's interface."
    studio_input_file: str = "The input file to modify based on the schema file."
    studio_port: str = "Specifies the studio server port."
    # secrets
    secret_create_value: str = "The value corresponding to the secret."
    secret_list_filter: str = "The query to filter the secrets by."
    # completion
    autocomplete_message: str = """\
        Generate command-completion configuration for KSDK commands.
        \b

        To configure your shell to complete KSDK commands:

        \b
            Bash:

                $ kelvin configuration autocomplete --shell bash > ~/.bashrc.ksdk
                $ echo "source ~/.bashrc.ksdk" >> ~/.bashrc

        \b
            ZSH:

                $ kelvin configuration autocomplete --shell zsh > ~/.zshrc.ksdk
                $ echo "source ~/.zshrc.ksdk" >> ~/.zshrc"""
    shell: str = "Name of the shell to generate completion configuration, e.g. bash, zsh, fish"
    # injector
    data_injector_app_name: str = "The app to inject data into."
    data_injector_endpoint: str = "The endpoint to publish."
    data_injector_poller_period: str = "The rate at which data will be polled from the application."
    data_injector_repeat: str = "Repeat data injection forever."
    data_injector_ignore_timestamps: str = "Ignore timestamps in data"
    # extractor
    data_extractor_batch: str = "The extractor batch write frequency."


class GeneralConfigs:
    # documentation link
    docs_url: str = "https://docs.kelvininc.com"
    # configuration files
    default_ksdk_history_file: str = "~/.config/kelvin/ksdk_history.log"
    default_ksdk_configuration_file: str = "~/.config/kelvin/ksdk.yaml"
    default_kelvin_sdk_client_configuration_file: str = "~/.config/kelvin/client.yaml"
    # default app names
    default_app_description: str = "Default description."
    default_app_version: str = "1.0.0"
    # dirs
    default_build_dir: str = "build"
    default_data_dir: str = "data"
    default_datamodel_dir: str = "datamodel"
    default_docs_dir: str = "docs"
    default_shared_dir: str = "shared"
    default_tests_dir: str = "tests"
    # files
    default_python_init_file: str = "__init__.py"
    default_python_main_file: str = "__main__.py"
    default_python_setup_file: str = "setup.py"
    default_python_test_file: str = "test_application.py"
    default_app_config_file: str = "app.yaml"
    default_migrated_app_config_file: str = "app.yaml"
    default_git_keep_file: str = ".keep"
    default_git_ignore_file: str = ".gitignore"
    default_docker_ignore_file: str = ".dockerignore"
    default_requirements_file: str = "requirements.txt"
    default_system_packages_file: str = "sys_requirements.txt"
    default_dockerfile: str = "Dockerfile"
    default_build_logs_file: str = "build.log"
    default_executable: str = "run_app"
    # cpp
    default_cmakelists_file: str = "CMakeLists.txt"
    default_makefile: str = "Makefile"
    # data images
    table_title: str = "*************************** {title} ***************************"
    # date visualization
    default_datetime_visualization_format: str = "%Y-%m-%d %H:%M:%S %z"
    default_datetime_and_elapsed_display: str = "{base_date}  ({now_minus_base_date})"
    # default env creation
    default_kelvin_app_dependency: str = "kelvin-app[data]==5.1.0"


class GeneralMessages:
    invalid_app_name: str = "The provided app name is not valid. \nErrors:\n{reason}"
    invalid_app_name_with_version: str = "Please provide a valid app name with a version: e.g. 'app:1.0.0'"
    no_data_yielded: str = "No data yielded."
    no_data_available: str = "No data yielded."
    are_you_sure_question: str = "\t    Are you sure? {prompt}"
    provide_a_valid_response: str = "Please provide a valid response. ['yes','y','no','n']\n"
    invalid_file_or_directory: str = "Please provide a valid file type and/or directory."
