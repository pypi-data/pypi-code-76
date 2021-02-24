import os
import json
import click
import logging
from pathlib import Path

logger=logging.getLogger('mldock')

class WorkingDirectoryManager:
    """Base config manager with basic read, write and update functionality.
    """
    def __init__(self, base_dir):
        self.base_dir = base_dir
        prompt_input = True

        if not self.file_exists(self.base_dir):
            prompt_input = click.prompt("File not found. Create?", default="yes")

            if prompt_input:
                self.base_dir.mkdir(parents=True, exist_ok=True)

        self.make_asset_dirs()

    def get_working_dir(self):
        return self.base_dir

    def make_asset_dirs(self):
        """Create the directory structure, if not exists
        """
        logger.debug("Creating assets directories in working dir {} .".format(self.base_dir))

        try:
            self.input_data_dir.mkdir(parents=False, exist_ok=True)
            self.input_config_dir.mkdir(parents=False, exist_ok=True)
            self.model_dir.mkdir(parents=False, exist_ok=True)
            self.output_data_dir.mkdir(parents=False, exist_ok=True)

        except Exception as exception:
            logger.error(exception)

    @staticmethod
    def file_exists(filename: str) -> bool:
        """Check if file exists

        Args:
            filename (str): path to file

        Returns:
            bool: whether file exists
        """
        return os.path.exists(filename)

    @property
    def input_data_dir(self):
        return Path(self.base_dir, 'data')

    @property
    def input_config_dir(self):
        return Path(self.base_dir, 'config')

    @property
    def model_dir(self):
        return Path(self.base_dir, 'model')
    
    @property
    def output_data_dir(self):
        return Path(self.base_dir, 'output')

class BaseConfigManager:
    """Base config manager with basic read, write and update functionality.
    """
    def __init__(self, filepath):
        self.filepath = filepath

        if not self.file_exists(self.filepath):
            prompt_input = click.prompt("File not found. Create?", default="yes")
        
            if prompt_input:
                self.touch(self.filepath)

        self.config = self.load_config(self.filepath)

    @staticmethod
    def touch(path: str):
        """create a blank json file, seeded with {}

        Args:
            path (str): path to file
        """
        with open(path, 'a') as file_:
            json.dump({}, file_)

    @staticmethod
    def file_exists(filename: str) -> bool:
        """Check if file exists

        Args:
            filename (str): path to file

        Returns:
            bool: whether file exists
        """
        return os.path.exists(filename)

    @staticmethod
    def load_config(filename: str) -> dict:
        """loads config from file

        Args:
            filename (str): path to config to load
        Returns:
            dict: config
        """
        with open(filename, "r") as file_:
            config = json.load(file_)
            return config

    def pretty_print(self):
        """pretty prints a json config to terminal
        """
        pretty_config = json.dumps(self.config, indent=4, separators=(',', ': '), sort_keys=True)
        logger.debug("{}\n".format(pretty_config))

    def write_file(self):
        """
        Trains ML model(s) locally
        :param dir: [str], source root directory
        :param docker_tag: [str], the Docker tag for the image
        :param image_name: [str], The name of the Docker image
        """

        with open(self.filepath, 'w') as config_file:
            json.dump(self.config, config_file, indent=4)

    def get_config(self) -> dict:
        """get config object

        Returns:
            dict: config
        """
        return self.config

class ResourceConfigManager(BaseConfigManager):
    """Resource Config Manager for mldock
    """
    config = {
        "current_host": "algo-1",
        "hosts": [
            "algo-1"
        ],
        "network_interface_name": "eth1"
    }

    @staticmethod
    def ask_for_current_host_name():
        """prompt user for current host name

        Returns:
            return: current host name
        """
        current_host_name = chosen_python_index = click.prompt(
            text="Set current host name: ",
            default="algo",
        )

        return current_host_name

    @staticmethod
    def ask_for_network_interface_name():
        """prompt user for network interface name

        Returns:
            str: network interface name
        """
        network_interface_name = click.prompt(
            text="Set current host name: ",
            default="eth1",
        )

        return network_interface_name

    def ask_for_resourceconfig(self):
        """prompt user for resource config
        """
        current_host_name = self.ask_for_current_host_name()
        hosts = [current_host_name+"-1"]
        network_interface_name = self.ask_for_network_interface_name()

        self.config = {
            "current_host": hosts[0],
            "hosts": hosts,
            "network_interface_name": network_interface_name
        }

class MLDockConfigManager(BaseConfigManager):
    """Hyperparameter Config Manager for mldock
    """

    config = {}

    def setup_config(self):

        self.ask_for_image_name()
        self.ask_for_platform_name()
        self.ask_for_mldock_module_dir()
        self.ask_for_container_dir_name()
        self.ask_for_requirements_file_name()

    def ask_for_image_name(self):
        """prompt user for image name
        """
        image_name = click.prompt(
            text="Set your image name: ",
            default=self.config.get('image_name', 'my_ml_container')
        )

        self.config.update({
            'image_name':image_name
        })
    
    def ask_for_platform_name(self):
        """prompt user for platform name
        """
        platform_name = click.prompt(
            text="Set your platform name:",
            default=self.config.get('platform', 'generic')
        )

        self.config.update({
            'platform': platform_name
        })

    def ask_for_container_dir_name(self):
        """prompt user for container dir name
        """
        container_dir_name = click.prompt(
            text="Set your container dir name:",
            default=self.config.get('container_dir', 'container')
        )

        self.config.update({
            'container_dir': container_dir_name
        })

    def ask_for_mldock_module_dir(self):
        """prompt user for mldock module dir
        """
        
        mldock_module_dir = click.prompt(
            text="Set mldock module dir: ",
            default=self.config.get('mldock_module_dir', 'src')
        )

        self.config.update({
            'mldock_module_dir': mldock_module_dir
        })

    def ask_for_requirements_file_name(self):
        """prompt user for image name
        """
        requirements_file_name = click.prompt(
            text="Set full path to requirements: ",
            default=self.config.get('requirements_dir', 'requirements.txt')
        )

        self.config.update({
            'requirements_dir':requirements_file_name
        })
    
    def update_stages(self, stages: dict):
        """"""
        self.config.update(
            {'stages': stages}
        )

    def update_env_vars(self, environment: dict):
        """
            Update environment node in .mldock config

            Args:
                environment (dict): key,value dictionaries
        """
        self.config.update(
            {'environment': environment}
        )

    def update_hyperparameters(self, hyperparameters: dict):
        """
            Update hyperparameter node in .mldock config

            Args:
                hyperparameters (dict): key,value dictionaries
        """
        self.config.update(
            {'hyperparameters': hyperparameters}
        )

    def update_data_channels(self, data: dict):
        """
            Update data node in .mldock config

            Args:
                data (dict): key,value dictionaries
        """
        self.config.update(
            {'data': data}
        )

class PackageConfigManager(BaseConfigManager):
    """Package Requirement Config Manager for sagify
    """
    @staticmethod
    def touch(filename):
        """creat an empty txt file

        Args:
            filename (str): path to file
        """
        Path(filename).touch()

    @staticmethod
    def load_config(filename: str) -> list:
        """load config

        Args:
            filename (str): path to config file to load

        Returns:
            list: config
        """
        path = Path(filename)
        with path.open() as f: 
            config = f.readlines()
        
        for index, c_package in enumerate(config):
            if c_package.endswith("\n"):
                config[index] = config[index].split("\n")[0]
        return config

    def get_config(self) -> list:
        """get config object

        Returns:
            list: config
        """
        return self.config

    def seed_packages(self, packages: list):
        """seeds config with required package modules

        Args:
            packages (list): packages to add to config
        """
        for new_package in packages:
            for config_package in self.config:
                if new_package not in config_package:
                    self.config.append(new_package)

    def pretty_print(self):
        """pretty prints a list config to terminal
        """
        pretty_config = json.dumps(self.config, indent=4, separators=(',', ': '))
        logger.debug("{}\n".format(pretty_config))

    def write_file(self):
        """
        write to file
        """
        config = set(self.config)
        config_txt = "\n".join(config) + "\n"
        Path(self.filepath).write_text(config_txt)

class StageConfigManager(BaseConfigManager):
    """Development Stage Config Manager for mldock
    """

    def __init__(self, config: dict):
        self.config = config

    def ask_for_stages(self):
        """prompt user for stages
        """
        while True:
            click.secho("Stages", bg='green', nl=True)
            click.secho("Add a stage by following the prompts", fg='green', nl=True)
            stage_name = click.prompt(
                text="Stage name: ",
                default="end",
                show_default=False,
                type=str
            )
            if stage_name == "end":
                break
            else:
                docker_tag = click.prompt(
                    text="Set docker image tag: ",
                    default=self.config.get(stage_name, {}).get('tag', None)
                )
                if stage_name not in self.config:
                    self.config[stage_name] = {}

                self.config[stage_name].update(
                    {'tag': docker_tag}
                )

class HyperparameterConfigManager(BaseConfigManager):
    """Hyperparameter Config Manager for mldock
    """

    def __init__(self, config: dict):
        self.config = config

    @staticmethod
    def is_float(s):
        """ Returns True is string is a number. """
        try:
            float(s)
            return True
        except ValueError:
            return False

    def ask_for_hyperparameters(self):
        """prompt user for hyperparameters
        """
        while True:
            name_value_pair = click.prompt(
                text="Add a hyperparameter. (Expects name:value). Hit enter to continue.",
                default="end",
                show_default=False,
                type=str
            )
            if name_value_pair == "end":
                break
            elif "=" in name_value_pair and not name_value_pair == "name=value":
                name, value = name_value_pair.split("=",1)
                if value.isdigit():
                    value = int(value)
                elif self.is_float(value):
                    value = float(value)
                logger.debug("Adding {}={}".format(name, value))
                self.config.update({name: value})
            else:
                logger.warning("Expected format as name=value. Skipping")

class EnvironmentConfigManager(BaseConfigManager):
    """Environment Config Manager for mldock
    """
    def __init__(self, config: dict):
        self.config = config

    @staticmethod
    def is_float(s):
        """ Returns True is string is a number. """
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def parse_bool(s):
        """ Returns True is string is a bool. """
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        else:
            return s

    def ask_for_env_vars(self):
        """prompt user for hyperparameters
        """
        while True:
            name_value_pair = click.prompt(
                text="Add a environment variable. (Expects name:value). Hit enter to continue.",
                default="end",
                show_default=False,
                type=str
            )
            if name_value_pair == "end":
                break
            elif "=" in name_value_pair and not name_value_pair == "name=value":
                name, value = name_value_pair.split("=",1)
                value = self.parse_bool(value)
                if isinstance(value, bool):
                    pass
                elif value.isdigit():
                    value = int(value)
                elif self.is_float(value):
                    value = float(value)
                logger.debug("Adding {}={}".format(name, value))
                self.config.update({name: value})
            else:
                logger.warning("Expected format as name=value. Skipping")

class InputDataConfigManager(BaseConfigManager):
    """InputData Config Manager for mldock
    """
    def __init__(self, config: dict):
        self.config = config

    def ask_for_input_data_channels(self):
        """prompt user for hyperparameters
        """
        while True:
            channel_filename_pair = click.prompt(
                text="Add a data channel. (Expects channel/filename). Hit enter to continue.",
                default="end",
                show_default=False,
                type=str
            )
            if channel_filename_pair == "end":
                logger.debug("\nUpdated data channels")
                self.pretty_print()
                break
            elif "/" in channel_filename_pair and not channel_filename_pair == "channel:filename":
                channel, filename = channel_filename_pair.split("/",1)
                logger.debug("Adding data/{}/{}".format(channel, filename))
                self.config.append({
                    'channel': channel,
                    'filename': filename
                })
            else:
                logger.warning("Expected format as channel/filename. Skipping")
